"""Prévias do gancho e do fechamento da REV2 (vlog de Bruges) com contador e o texto da narração na tela, para o Diego
gravar olhando para elas (mesmo modelo de Amsterdam e Bruxelas: `docs/VIDEO_LONGO_YOUTUBE.md`, seção 5, passo 3).

Roda de reels/bruges-yt, com o proxy servido em 127.0.0.1:8787
(node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787):

    python -I rev2/previas_narracao_rev2.py            # props + render + mixagem das duas prévias
    python -I rev2/previas_narracao_rev2.py --so-props

Saída: rev2/previas/rev2_gancho.mp4 e rev2/previas/rev2_fechamento.mp4 (960 × 540, H.264 + AAC), e os props em
rev2/props_rev2_previa_{gancho,fechamento}.json.

Som da prévia: as falas reais (Marina no gancho, a chegada e o fim do corpo) e os efeitos do DS. A narração aparece só
como texto (a gravar). REV2: sem o `keen` no fim do gancho (Diego, 21/11/2026: "tire o efeito keen no início do vídeo").
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("roteiro_rev2", os.path.join(AQUI, "roteiro_rev2.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

FPS = R.FPS
SR = 48000
VIDEO = "http://127.0.0.1:8787/proxy1080.mp4"
RM = "../../design-system/remotion"
KEEN = "../../design-system/sons/externos/keen.wav"
KEEN_PICO = 0.96
TELA_FINAL_PREVIA = 8000
VALOR_CA2 = None  # REV2: a 2ª ida ao Chez Albert tem valor (€ 4,70, Diego, 21/11/2026)


def fmt(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def eur(v):
    return "€ " + fmt(v)


def brl(v):
    return "R$ " + fmt(v)


def q(ms):
    return round(ms * FPS / 1000)


def numeros():
    c = R.contas(VALOR_CA2)
    return c, {"gastos": f"{round(c['gastos'])}", "total": f"{round(c['total'])}", "pp": f"{round(c['pp'])}", "pp_brl": f"{round(c['pp_brl'])}"}


def sequencia(lista, gap=350):
    """Tempos (ms) de cada bloco: `em` fixo ou 0,35 s depois do fim estimado do anterior."""
    _, num = numeros()
    out, fim = [], None
    for n in lista:
        texto = n["texto"].format(**num)
        em = n["em"] if n["em"] is not None else fim + gap
        dur = R.dur_estimada(texto) * 1000
        if fim is not None:
            assert em >= fim + 150, f"{n['id']} começa antes do fim estimado do bloco anterior ({(fim - em) / 1000:.2f} s)"
        out.append({"id": n["id"], "ini": em, "fim": em + dur, "texto": texto})
        fim = em + dur
    return out


def trechos_de(takes, base=0.0):
    tr, pos = [], base
    for t in takes:
        dur = (t["ate"] - t["de"]) * 1000
        assert dur >= 2000, f"take com menos de 2 s: {t}"
        tr.append({"src": round(t["de"] * 1000), "de": round(pos), "ate": round(pos + dur), "som": t.get("som", "baixo")})
        pos += dur
    return tr, pos


def props_gancho():
    tr, G = trechos_de(R.GANCHO)
    chegada_dur = 6000
    tr.append({"src": round(R.CHEGADA[0] * 1000), "de": round(G), "ate": round(G + chegada_dur), "som": "fala"})
    narr = sequencia(R.NARRACAO_GANCHO)
    marina = next(t for t in tr if t["som"] == "fala")
    for n in narr:
        assert not (n["ini"] < marina["ate"] and n["fim"] > marina["de"]), f"{n['id']} cai em cima da fala da Marina"
        assert n["fim"] <= G, f"{n['id']} passa do gancho"
    ev = []
    # compra do bilhete: Recibo (pedido do Diego: "18 euros por trecho por pessoa") + Placar, no "E a conta começa aqui"
    g = R.GASTOS[0]
    t_rec = narr[-1]["ini"] + 250
    total = sum(v for _, v in g["linhas"])
    ev.append({"tipo": "placar", "ligar": t_rec - 200, "desligar": t_rec + 3400,
               "valores": [{"em": t_rec - 200, "tempo": g["hora"], "gasto": eur(0)}, {"em": t_rec + 400, "tempo": g["hora"], "gasto": eur(total)}]})
    ev.append({"tipo": "recibo", "lugar": g["lugar"], "cabecalho": f"SEG 16/03 · {g['hora'].replace(':', 'H')} · € 18 POR TRECHO/PESSOA",
               "linhas": [[a, eur(v)] for a, v in g["linhas"]], "total": eur(total), "real": "≈ " + brl(total * R.COTACAO),
               "rodape": R.RODAPE, "ini": t_rec, "fim": G + 300, "x": 1400, "y": 150, "escala": 0.72})
    assert t_rec + 3400 + 240 <= G + 1000, "o Placar não apaga antes da data"
    ev.append({"tipo": "placa", "rotulo": "1 DIA EM", "destino": "BRUGES", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": G + 500, "saida": G + 4200})
    ev.append({"tipo": "data", "texto": R.DATA, "ini": G + 1000, "fim": G + 4600})
    frases = [{"ini": n["ini"], "fim": n["fim"], "texto": f"{n['id']} · {n['texto']}"} for n in narr]
    frases.append({"ini": marina["de"], "fim": marina["ate"], "texto": "(fala real da Marina, não narrar)"})
    frases.sort(key=lambda f: f["ini"])
    ev.append({"tipo": "guia", "inicio": 0, "fim": G, "frases": frases})
    dur = G + chegada_dur
    return {"video": VIDEO, "duracao": dur, "fps": FPS, "trechos": [{k: v for k, v in t.items() if k != "som"} for t in tr], "eventos": ev, "zooms": [], "refLufs": -16}, tr, narr, G


def props_fechamento():
    antes = 6000
    tr = [{"src": round((R.FIM_CORPO - antes / 1000) * 1000), "de": 0, "ate": antes, "som": "fala"}]
    tf, F = trechos_de(R.FECHAMENTO, base=antes)
    tr += tf
    narr = sequencia(R.NARRACAO_FECHAMENTO)
    for n in narr:
        n["ini"] += antes
        n["fim"] += antes
    assert narr[-1]["fim"] + 500 <= F, f"a F7 passa do fim dos planos ({(narr[-1]['fim'] + 500 - F) / 1000:.2f} s)"
    tr[-1]["pagina"] = True  # a última cena vira a página para a tela final
    c, num = numeros()
    by = {n["id"]: n for n in narr}
    ev = []
    gastos, hotel, total, pp = c["gastos"], c["hotel"], c["total"], c["pp"]
    t_rec = by["F4"]["ini"] - 200
    t_hot = by["F5"]["ini"] - 100
    cat = {"comida": 0.0, "transporte": 0.0}
    for g in R.GASTOS:
        for _, v in g["linhas"]:
            cat[g["cat"]] += VALOR_CA2 if v is None else v
    ev.append({"tipo": "recibo", "lugar": "1 DIA EM BRUGES", "cabecalho": "SEG 16/03 · 2 PESSOAS · SEM PASSAGEM AÉREA",
               "linhas": [["Comida e bebida", eur(cat["comida"])], ["Trem (ida e volta)", eur(cat["transporte"])], ["Hotel (1 noite)", eur(hotel)]],
               "total": eur(total), "real": f"{eur(pp)}/pessoa ≈ {brl(c['pp_brl'])}", "rodape": R.RODAPE, "ini": t_rec, "fim": by["F5"]["fim"] + 900,
               "x": 1360, "y": 96, "escala": 0.78, "aparecer": [0, 0, round(t_hot - t_rec)],
               "totais": [{"total": eur(gastos), "real": f"{eur(gastos / 2)}/pessoa"}, {"total": eur(gastos), "real": f"{eur(gastos / 2)}/pessoa"},
                          {"total": eur(total), "real": f"{eur(pp)}/pessoa ≈ {brl(c['pp_brl'])}"}]})
    t_bil = by["F6"]["ini"] + 900
    ev.append({"tipo": "bilhete", "texto": "vale muito!|voltaria mil vezes", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": t_bil, "saida": by["F6"]["fim"] + 600})
    ev.append({"tipo": "nota", "titulo": "Basílica do Sangue Sagrado", "linhas": ["entrada grátis", "relíquia exposta: 14h às 16h"], "ini": by["F7"]["ini"] + 600, "fim": by["F7"]["fim"] + 700,
               "x": 1270, "y": 140, "largura": 560, "icone": "dica"})
    t_like = by["F8"]["ini"] + 1300
    ev.append({"tipo": "like", "entrada": t_like, "saida": t_like + 3300})
    t_ig = t_like + 3300 + 250  # a placa do like sai antes (240 ms) de a chamada do Instagram entrar
    ev.append({"tipo": "instagram", "ini": t_ig, "fim": by["F8"]["fim"] + 700})
    t_placa = by["F9"]["ini"]
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": t_placa, "saida": F - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": t_placa + 400, "relDb": -12})
    ev.append({"tipo": "telafinal", "ini": F, "proximo": R.PROXIMO})
    frases = [{"ini": n["ini"], "fim": n["fim"], "texto": f"{n['id']} · {n['texto']}"} for n in narr]
    ev.append({"tipo": "guia", "inicio": antes, "fim": F, "topo": True, "frases": frases})
    dur = F + TELA_FINAL_PREVIA
    return {"video": VIDEO, "duracao": dur, "fps": FPS, "trechos": [{k: v for k, v in t.items() if k != "som"} for t in tr], "eventos": ev, "zooms": [], "refLufs": -16}, tr, narr, F


def mixar(tr, dur_ms, sfx_wav, saida, keen_em=None):
    """Falas reais da fonte (só os trechos `fala`) + efeitos do render + keen; −16 LUFS, pico ≤ −1 dBFS."""
    voz, sr = sf.read("_tmp/voz_orig.wav", dtype="float32", always_2d=True)
    assert sr == SR
    n = int(round(dur_ms / 1000 * SR))
    out = np.zeros((n, 2), dtype=np.float32)
    rampa = int(0.012 * SR)
    for t in tr:
        if t["som"] != "fala":
            continue
        a = int(round(t["src"] / 1000 * SR))
        d0, d1 = int(round(t["de"] / 1000 * SR)), int(round(t["ate"] / 1000 * SR))
        pedaco = voz[a:a + (d1 - d0)].copy()
        env = np.ones(len(pedaco), dtype=np.float32)
        env[:rampa] = np.linspace(0, 1, rampa)
        env[-rampa:] = np.linspace(1, 0, rampa)
        out[d0:d0 + len(pedaco)] += pedaco * env[:, None]
    medidor = pyln.Meter(SR)
    lv = medidor.integrated_loudness(out) if np.abs(out).max() > 0 else -70
    out *= 10 ** ((-20.0 - lv) / 20)
    if keen_em is not None:
        k, ksr = sf.read(KEEN, dtype="float32", always_2d=True)
        if ksr != SR:
            idx = np.arange(0, len(k), ksr / SR)
            k = np.stack([np.interp(idx, np.arange(len(k)), k[:, c]) for c in range(k.shape[1])], axis=1).astype(np.float32)
        if k.shape[1] == 1:
            k = np.repeat(k, 2, axis=1)
        lk = medidor.integrated_loudness(k)
        k *= 10 ** ((-26.0 - lk) / 20)  # −6 dB da voz (−20 LUFS), volume de trabalho do keen
        i0 = int(round((keen_em / 1000 - KEEN_PICO) * SR))
        j0 = max(0, -i0)
        i0 = max(0, i0)
        m = min(len(k) - j0, n - i0)
        out[i0:i0 + m] += k[j0:j0 + m]
    s, ssr = sf.read(sfx_wav, dtype="float32", always_2d=True)
    m = min(len(s), n)
    out[:m] += s[:m]
    lt = medidor.integrated_loudness(out)
    out *= 10 ** ((-16.0 - lt) / 20)
    pico = np.abs(out).max()
    if pico > 0.89:
        out *= 0.89 / pico
    sf.write(saida, out, SR, subtype="FLOAT")


def render(nome, props, tr, dur_ms, keen_em=None):
    arq = f"rev2/props_rev2_previa_{nome}.json"
    os.makedirs("_tmp/previas", exist_ok=True)
    os.makedirs("rev2/previas", exist_ok=True)
    mp4 = f"_tmp/previas/{nome}.render.mp4"
    q1 = q(dur_ms) - 1
    env = dict(os.environ, CRF="24", X264_PRESET="veryfast", TMPDIR=os.path.abspath("_tmp/rtmp"))
    os.makedirs("_tmp/rtmp", exist_ok=True)
    subprocess.run(["node", "scripts/videolongo.mjs", f"../../reels/bruges-yt/{arq}", "../../reels/bruges-yt/public", "trecho",
                    f"../../reels/bruges-yt/{mp4}", "0", str(q1), "0.5"], cwd=RM, env=env, check=True)
    sfx = f"_tmp/previas/{nome}.sfx.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", mp4, "-map", "0:a", "-ar", str(SR), "-ac", "2", "-c:a", "pcm_f32le", sfx], check=True)
    mix = f"_tmp/previas/{nome}.mix.wav"
    mixar(tr, dur_ms, sfx, mix, keen_em)
    saida = f"rev2/previas/rev2_{nome}.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", mp4, "-i", mix, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "27", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", saida], check=True)
    print("ok", saida, os.path.getsize(saida) // 1024, "KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-props", action="store_true")
    ap.add_argument("quais", nargs="*", default=["gancho", "fechamento"])
    a = ap.parse_args()
    pg, trg, ng, G = props_gancho()
    pf, trf, nf, F = props_fechamento()
    json.dump(pg, open("rev2/props_rev2_previa_gancho.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(pf, open("rev2/props_rev2_previa_fechamento.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"gancho_ms": G, "fechamento_ms": F - 6000, "narracao_gancho": ng, "narracao_fechamento": nf, "contas_previa": R.contas(VALOR_CA2)},
              open("rev2/tempos_narracao_rev2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"gancho {G / 1000:.2f} s · fechamento {(F - 6000) / 1000:.2f} s")
    for n in ng + nf:
        print(f"  {n['id']}  {n['ini'] / 1000:6.2f}–{n['fim'] / 1000:6.2f}  {n['texto']}")
    if a.so_props:
        return
    if "gancho" in a.quais:
        render("gancho", pg, trg, pg["duracao"])
    if "fechamento" in a.quais:
        render("fechamento", pf, trf, pf["duracao"])


if __name__ == "__main__":
    sys.exit(main())
