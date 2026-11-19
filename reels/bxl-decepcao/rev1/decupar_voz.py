"""Decupagem da voz do Reel BXL-decepção (REV1).

Roda de reels/bxl-decepcao:  python3 rev1/decupar_voz.py

Entrada
  fonte/audio/audio_1..7.m4a          os 7 áudios gravados pelo Diego (Drive: Bruxelas/Reel/Decepcao,
                                      "Praça Ernesto Lebram", "… 2" … "… 7", na ordem do nome)
  fonte/transcricao_large-v3.json     transcrição automática com tempo por palavra (faster-whisper large-v3)

Saída
  _tmp/voz_decupada.wav               voz contínua, 48 kHz mono, sem silêncios longos (antes do master)
  rev1/voz_rev1.json                  trechos usados (arquivo, entrada, saída, início no Reel) e palavras
                                      com o tempo no Reel (base das âncoras de cena e das legendas)

Regras (docs/FORMATOS_REELS.md, 10.1; CLAUDE.md, 12):
  - corte sempre no silêncio: início e fim da fala medidos pela energia na faixa 120–4.000 Hz;
  - pausas internas acima de 0,30 s viram 0,20 s (o corte cai no meio do silêncio, nunca na palavra);
  - entre um áudio e o próximo, pausa total de ≈ 0,26 s (≈ 0,30 s quando muda o assunto: respiro curto);
  - nada de acelerar a voz; nenhuma palavra cortada; fade de 25 ms nas emendas;
  - estalos curtos depois da última palavra (≤ 0,2 s, fora da transcrição) ficam de fora.
A validação auditiva é humana: o Claude não escuta áudio.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
PRE = 0.05          # folga antes do início da fala
POS = 0.12          # folga depois do fim da fala
PAUSA_MAX = 0.30    # pausa interna acima disso é encurtada
PAUSA_NOVA = 0.20
EMENDA = 0.12       # silêncio inserido entre dois áudios (somado às folgas, dá ≈ 0,26 s de pausa)
EMENDA_ASSUNTO = 0.20
FADE = 0.025
ARQUIVOS = [f"audio_{i}.m4a" for i in range(1, 8)]
# depois de qual áudio o assunto muda (respiro um pouco maior): gancho→contexto, Manneken→"Mas…",
# "sensação que eu tive"→"Até que…", Bruges→"Não é que…", comparação→CTA falado
MUDA_ASSUNTO = {"audio_1.m4a", "audio_3.m4a", "audio_4.m4a", "audio_5.m4a", "audio_6.m4a"}


def ler(caminho):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).astype(np.float64)


def regioes_fala(a):
    sos = butter(4, [120, 4000], btype="band", fs=SR, output="sos")
    b = sosfilt(sos, a)
    hop = int(SR * 0.01)
    n = len(b) // hop
    rms = np.sqrt(np.array([np.mean(b[k * hop:(k + 1) * hop] ** 2) for k in range(n)]) + 1e-12)
    db = 20 * np.log10(rms)
    piso, pico = np.percentile(db, 5), np.percentile(db, 98)
    lim = max(piso + 12, pico - 38)
    reg, on = [], None
    for k, v in enumerate(db > lim):
        if v and on is None:
            on = k
        elif not v and on is not None:
            reg.append([on / 100, k / 100])
            on = None
    if on is not None:
        reg.append([on / 100, n / 100])
    junt = []
    for r in reg:
        if junt and r[0] - junt[-1][1] < 0.12:
            junt[-1][1] = r[1]
        else:
            junt.append(r)
    return [r for r in junt if r[1] - r[0] >= 0.04], float(lim)


def main():
    raiz = os.getcwd()
    if not os.path.isdir(os.path.join(raiz, "fonte", "audio")):
        sys.exit("rode de reels/bxl-decepcao")
    trans = json.load(open("fonte/transcricao_large-v3.json"))
    os.makedirs("_tmp", exist_ok=True)

    saida, trechos, vistas = [], [], {}
    t_reel = 0.0
    for i, nome in enumerate(ARQUIVOS):
        a = ler(os.path.join("fonte", "audio", nome))
        dur = len(a) / SR
        regs, lim = regioes_fala(a)
        ws = trans[f"a{i + 1}.wav"]["words"]
        fim_ultima = max(w["e"] for w in ws)
        # estalo depois da última palavra: região curta que começa depois do fim da transcrição
        regs = [r for r in regs if not (r[0] > fim_ultima - 0.05 and r[1] - r[0] <= 0.2)]
        ini = max(0.0, regs[0][0] - PRE)
        fim = min(dur, regs[-1][1] + POS)
        # blocos mantidos dentro do arquivo: pausas longas encurtadas no meio do silêncio
        blocos = [[ini, None]]
        for r0, r1 in zip(regs, regs[1:]):
            gap = r1[0] - r0[1]
            if gap > PAUSA_MAX:
                meio = PAUSA_NOVA / 2
                blocos[-1][1] = r0[1] + meio
                blocos.append([r1[0] - meio, None])
        blocos[-1][1] = fim
        # ganho para igualar a voz entre os arquivos (RMS da fala)
        fala = np.concatenate([a[int(r[0] * SR):int(r[1] * SR)] for r in regs])
        rms = float(np.sqrt(np.mean(fala ** 2)))
        for k, (b0, b1) in enumerate(blocos):
            folga = PRE if k == 0 else PAUSA_NOVA / 2  # a fala começa esta distância depois do início do bloco
            seg = a[int(b0 * SR):int(b1 * SR)].copy()
            nf = int(FADE * SR)
            seg[:nf] *= np.linspace(0, 1, nf)
            seg[-nf:] *= np.linspace(1, 0, nf)
            saida.append(("voz", seg, rms))
            trechos.append({"arquivo": nome, "entrada": round(b0, 3), "saida": round(b1, 3), "inicio_reel": round(t_reel, 3)})
            # palavras dentro do bloco. Uma palavra que o Whisper estica por cima de um corte aparece nos dois
            # blocos: vale o bloco seguinte (onde a energia mostra a fala de fato)
            for j, w in enumerate(ws):
                if (w["e"] > b0 + 0.02 or (k == 0 and j == 0)) and w["s"] < b1:
                    # o Whisper adianta a 1ª palavra depois de um silêncio: nunca antes do início medido da fala
                    s = max(w["s"], b0 + folga) - b0 + t_reel
                    e = max(min(w["e"], b1) - b0 + t_reel, s + 0.06)
                    vistas[(nome, j)] = {"w": w["w"].strip(), "s": round(s, 3), "e": round(e, 3), "p": w["p"], "arquivo": nome}
            t_reel += b1 - b0
        if i < len(ARQUIVOS) - 1:
            pausa = EMENDA_ASSUNTO if nome in MUDA_ASSUNTO else EMENDA
            saida.append(("sil", np.zeros(int(pausa * SR)), None))
            t_reel += pausa
        print(f"{nome}: {dur:.2f}s → {sum(b1 - b0 for b0, b1 in blocos):.2f}s ({len(blocos)} blocos, limiar {lim:.1f} dB, rms {20*np.log10(rms):.1f} dB)")

    palavras = sorted(vistas.values(), key=lambda p: p["s"])
    ref = np.median([r for k, _, r in saida if k == "voz"])
    pecas = [seg * (ref / r) if k == "voz" else seg for k, seg, r in saida]
    voz = np.concatenate(pecas)
    # passa-alta 70 Hz (FORMATOS_REELS 10.1); a redução de ruído leve e o loudness ficam na mixagem
    voz = sosfilt(butter(2, 70, btype="high", fs=SR, output="sos"), voz)
    sf.write("_tmp/voz_decupada.wav", voz.astype(np.float32), SR, subtype="FLOAT")

    json.dump({"duracao": round(len(voz) / SR, 3), "trechos": trechos, "palavras": palavras},
              open("rev1/voz_rev1.json", "w"), ensure_ascii=False, indent=1)
    print(f"voz decupada: {len(voz) / SR:.2f} s · {len(palavras)} palavras")


if __name__ == "__main__":
    main()
