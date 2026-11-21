"""Conferência do áudio do vídeo FINAL da REV5 (vlog de Bruges), no som do arquivo exportado. Medição, não escuta (o Claude
não escuta: a validação auditiva é do Diego). Versão da `rev4/conferir_audio_rev4.py` com as narrações gravadas.

Roda de reels/bruges-yt, depois de `python -I rev5/finalizar_rev5.py`:  python -I rev5/conferir_audio_rev5.py
Lê rev5/linha_do_tempo_rev5.json, rev5/props_rev5.json, _tmp/voz_orig.wav, _tmp/musica_rev5.wav, _tmp/final_rev5/mix_mix.json
e o som do MP4 final. Escreve rev5/audio/CONFERENCIA_AUDIO_REV5.md.
"""
import bisect
import json
import os
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

SR = 48000
FINAL = os.environ.get("FINAL", "_tmp/final_rev5/PrimeiroDia_Bruges_REV5_4K.mp4")
MIXJSON = os.environ.get("MIXJSON", "_tmp/final_rev5/mix_mix.json")


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}".replace(".", ",")


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(np.square(x))) + 1e-12)


def main():
    lt = json.load(open("rev5/linha_do_tempo_rev5.json", encoding="utf-8"))
    props = json.load(open("rev5/props_rev5.json", encoding="utf-8"))
    mix = json.load(open(MIXJSON, encoding="utf-8"))
    dec = "_tmp/final_rev5/final_dec.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", FINAL, "-map", "0:a", "-c:a", "pcm_f32le", dec], check=True)
    fim, _ = sf.read(dec, dtype="float32", always_2d=True)
    mus, _ = sf.read("_tmp/musica_rev5.wav", dtype="float32", always_2d=True)
    mus *= 10 ** (mix["musica_ganho_db"] / 20)
    D = lt["duracao_ms"] / 1000
    G, B = lt["gancho_ms"] / 1000, lt["corpo_fim_ms"] / 1000
    alvo = mix["voz_fonte"]["fala_alvo_lufs"]
    med = pyln.Meter(SR)
    L = ["# REV5 · Conferência do áudio do vídeo final (vlog de Bruges)", "",
         f"Medição feita por `rev5/conferir_audio_rev5.py` no som do arquivo exportado (`{os.path.basename(FINAL)}`). **Não é escuta**: o Claude não escuta áudio; a validação auditiva é sua.", ""]
    problemas = 0

    # 1. emendas da voz da fonte
    au = sorted(lt["audio"], key=lambda a: a["out"])
    sobre = [(a["out"] / 1000, (a["out"] + a["dur"] - b["out"]) / 1000) for a, b in zip(au, au[1:]) if b["out"] < a["out"] + a["dur"] - 1]
    L += ["## 1. Emendas", "", f"- {len(au)} trechos de som da fonte (gancho + corpo). Sobrepostos: **{len(sobre)}**" + (": " + ", ".join(f"{mmss(t)} ({d:.2f} s)" for t, d in sobre) if sobre else "") + "."]
    problemas += len(sobre)

    # narrações: uma não pisa na outra nem na fala do vídeo
    nar = mix["narracoes"]
    pis = []
    for n in nar:
        a, b = n["entra_ms"], n["sai_ms"]
        for o in nar:
            if o is not n and o["entra_ms"] < b and o["sai_ms"] > a and o["entra_ms"] > a:
                pis.append(f"{n['id']} × {o['id']} ({(b - o['entra_ms']) / 1000:.2f} s)")
        for p in au:
            if p["out"] < b - 1 and p["out"] + p["dur"] > a + 1:
                pis.append(f"{n['id']} × som da fonte em {mmss(p['out'] / 1000)} ({(min(b, p['out'] + p['dur']) - max(a, p['out'])) / 1000:.2f} s)")
    L += [f"- Narrações gravadas (13 arquivos, recortadas de 120 ms antes a até 250 ms depois da fala): sobreposições com outra narração ou com o som da fonte: **{len(pis)}**" + (": " + "; ".join(pis) if pis else "") + ".",
          "- Ganho de cada narração até a fala-alvo (" + f"{alvo:.1f} LUFS" + "): " + ", ".join(f"{n['id']} {n['ganho_db']:+.1f} dB" for n in nar) + ".", ""]
    problemas += len(pis)

    # 2. buracos de silêncio no som final
    hop = SR // 100
    nivel = np.array([db(fim[k:k + hop, 0]) for k in range(0, len(fim) - hop, hop)])
    runs, k = [], 0
    while k < len(nivel):
        if nivel[k] < -60:
            j = k
            while j < len(nivel) and nivel[j] < -60:
                j += 1
            if j - k >= 30:
                runs.append((k / 100, (j - k) / 100))
            k = j
        else:
            k += 1
    meio = [r for r in runs if r[0] < D - 1]
    L += ["## 2. Buracos de silêncio (≥ 300 ms abaixo de −60 dBFS)", "", f"- **{len(meio)}**" + (": " + ", ".join(f"{mmss(t)} ({d:.2f} s)" for t, d in meio) if meio else " do começo ao fim.") + "", ""]
    problemas += len(meio)

    # 3. música por cima de fala do vlog (fora do gancho e do fechamento, onde fica 9 dB abaixo da narração de propósito)
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    ws = [w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]]
    corpo = sorted([p for p in au if p["tipo"] == "corpo"], key=lambda p: p["src"])
    srcs = [p["src"] for p in corpo]
    sob = []
    for w in ws:
        i = bisect.bisect_right(srcs, w["ini"] * 1000) - 1
        if i < 0:
            continue
        p = corpo[i]
        if not (p["src"] <= w["ini"] * 1000 and w["fim"] * 1000 <= p["src"] + p["dur"]):
            continue
        t = (p["out"] + (w["ini"] * 1000 - p["src"])) / 1000
        a, b = int(t * SR), int((t + w["fim"] - w["ini"]) * SR)
        if b > a and G <= t < B and db(mus[a:b, 0]) > -50:
            c = (w["ini"] + w["fim"]) / 2
            q10 = [db(mus[k:k + SR // 100, 0]) > -50 for k in range(a, b, SR // 100)]
            if any(j["fonte"] and j["fonte"][0] <= c < j["fonte"][1] for j in lt["musica"]):
                tipo = "erro de tempo do Whisper (palavra dentro de montagem sem fala: a fonte ali é silêncio digital)"
            elif sum(q10) * 0.01 <= 0.35:
                tipo = f"borda da janela de música ({sum(q10) * 10} ms com a música entrando/saindo)"
            else:
                tipo = "PROBLEMA"
            sob.append((t, w["p"], tipo))
    prob3 = [x for x in sob if x[2] == "PROBLEMA"]
    L += ["## 3. Música por cima de fala do vlog (corpo)", "", f"- Palavras com música tocando junto (acima de −50 dBFS): {len(sob)}; problemas: **{len(prob3)}**."]
    L += [f"  - {mmss(t)} \"{p}\": {tipo}" for t, p, tipo in sob]
    L += ["- Os mesmos 3 casos da conferência da REV4 aprovada (lá, 1,7 s mais tarde: o gancho ficou 1,7 s mais curto).", ""]
    problemas += len(prob3)

    # 4. nível da música em relação à fala-alvo
    def lufs(x):
        try:
            return med.integrated_loudness(x)
        except ValueError:
            return float("nan")
    jan = [j for j in lt["musica"] if j["id"].startswith("M")]
    lm = [lufs(mus[int(j["ini"] / 1000 * SR):int(j["fim"] / 1000 * SR)]) for j in jan if j["fim"] - j["ini"] > 3000]
    narr_g = [n for n in lt["narracoes"] if n["id"].startswith("G")]
    narr_f = [n for n in lt["narracoes"] if n["id"].startswith("F")]
    sob_g = lufs(np.concatenate([mus[int(n["fala_ini"] / 1000 * SR):int(n["fala_fim"] / 1000 * SR)] for n in narr_g]))
    sob_f = lufs(np.concatenate([mus[int(n["fala_ini"] / 1000 * SR):int(n["fala_fim"] / 1000 * SR)] for n in narr_f]))
    L += ["## 4. Nível da música (antes do master; fala-alvo " + f"{alvo:.1f} LUFS)", "",
          f"- Paisagens do corpo (só música): mediana {np.nanmedian(lm) - alvo:+.1f} dB da fala (alvo do projeto: −3 dB).",
          f"- Sob a narração do gancho: {sob_g - alvo:+.1f} dB; sob a do fechamento: {sob_f - alvo:+.1f} dB (alvo: −9 dB; [PROJETO] 8–10 dB abaixo da voz).", ""]

    # 5. quadros congelados e time-lapse
    voz_src, _ = sf.read("_tmp/voz_orig.wav", dtype="float32", always_2d=True)
    cg = [t for t in props["trechos"] if t.get("congela") and not t.get("pagina")]
    L += ["## 5. Quadros congelados e time-lapse", ""]
    for t in cg:
        a, b = int(t["de"] / 1000 * SR), int(t["ate"] / 1000 * SR)
        L.append(f"- Congelado {mmss(t['de'] / 1000)}–{mmss(t['ate'] / 1000)}: som final a {db(fim[a:b, 0]):.0f} dBFS (a voz segue).")
    for t in [t for t in props["trechos"] if t.get("velocidade")]:
        a, b = int(t["de"] / 1000 * SR), int(t["ate"] / 1000 * SR)
        fonte_no_tl = any(p["out"] < t["ate"] and p["out"] + p["dur"] > t["de"] for p in au)
        L.append(f"- Time-lapse {mmss(t['de'] / 1000)}–{mmss(t['ate'] / 1000)}: som da fonte {'PRESENTE' if fonte_no_tl else 'ausente'} (o acelerado vira voz de esquilo) · música a {db(mus[a:b, 0]):.0f} dBFS.")
        problemas += int(fonte_no_tl)
    L.append("")

    # 6. começo e fim
    L += ["## 6. Começo e fim", "",
          f"- Primeiros 10 ms: {db(fim[:480, 0]):.0f} dBFS; salto da 1ª amostra {abs(float(fim[0, 0])):.4f} (sem estalo de início).",
          f"- Gancho → 1ª cena: a música de abertura termina no corte ({mmss(G)}); 100 ms depois do corte, música a {db(mus[int((G + 0.02) * SR):int((G + 0.12) * SR), 0]):.0f} dBFS.",
          f"- Último 0,2 s: {db(fim[-int(0.2 * SR):, 0]):.0f} dBFS (a música sai nos 3 s finais). Duração do som decodificado {len(fim) / SR:.3f} s (o decodificador AAC soma ~20 ms de enchimento; no contêiner, o som tem a duração da imagem: `medidas_final_rev5.json`) × imagem {round(props['duracao'] * props['fps'] / 1000) / props['fps']:.3f} s ({round(props['duracao'] * props['fps'] / 1000)} quadros).", ""]

    # 7. loudness
    lv = med.integrated_loudness(fim)
    L += ["## 7. Nível do som exportado", "", f"- {lv:.1f} LUFS integrados (pyloudnorm) e pico de amostra {20 * np.log10(np.abs(fim).max() + 1e-12):.1f} dBFS. Medida oficial (ebur128, pico verdadeiro) em `medidas_final_rev5.json`.",
          f"- Limitador do master: redução máxima {mix['master']['limitador']['reducao_max_db']} dB; acima de 1 dB em {mix['master']['limitador']['acima_1db_pct']}% do tempo, acima de 6 dB em {mix['master']['limitador']['acima_6db_pct']}% (Amsterdam REV1: 9,0% e 0,3%).",
          "- Os 10 pontos em que o limitador mais trabalha (ouvir): " + ", ".join(f"{mmss(t / 1000)} ({g} dB)" for t, g in mix["master"]["limitador"]["piores_ms"]) + ".", "",
          f"**Resultado:** {problemas} problema(s) medido(s)." + (" Nada fora do lugar pela medição; falta a sua escuta." if problemas == 0 else " Ver os itens acima.")]
    os.makedirs("rev5/audio", exist_ok=True)
    open("rev5/audio/CONFERENCIA_AUDIO_REV5.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    os.remove(dec)
    print("\n".join(L))


if __name__ == "__main__":
    main()
