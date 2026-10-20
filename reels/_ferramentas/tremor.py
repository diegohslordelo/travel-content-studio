#!/usr/bin/env python3
"""Tremor de câmera em clipes já recortados para o Reel (1080 × 1920).

Mede o deslocamento global entre quadros vizinhos (correlação de fase) e separa o movimento intencional
(panorâmica, caminhada: a velocidade média em ~0,25 s) da tremedeira (o que sobra, em px por quadro). O recorte 9:16
amplia o tremor do bruto; por isso a medida é feita no plano já recortado, em px do Reel.

Regra (pedido do Diego, 20/10/2026): vale para todos os Reels. Plano com tremor RMS acima de LIMITE_RMS px, ou
com algum salto acima de LIMITE_PICO px entre quadros, é trocado ou encurtado para um trecho estável.
Limite da medida: não vê tremor de rotação nem câmera andando para a frente; conferir sempre no olho.

uso: python3 tremor.py arquivo.mp4 [...]                  # um relatório por arquivo
     python3 tremor.py --janela 1.5 arquivo.mp4 [...]     # também a janela mais estável de 1,5 s
Em Python: tremor(bruto, janela=1.5, filtro="crop=1216:2160:1300:0") mede o bruto já com o recorte do Reel.
"""
import json
import subprocess
import sys

import numpy as np

LIMITE_RMS = 2.0   # px do Reel
LIMITE_PICO = 6.0  # px do Reel
LARG = 270         # largura de análise (1080 / 4)


def quadros(arq, filtro=None):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                        "-of", "json", arq], capture_output=True, text=True)
    s = json.loads(r.stdout)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    if filtro:  # recorte do Reel aplicado ao bruto (ex.: "crop=1216:2160:1300:0"); a saída é sempre 9:16
        alt, vf, fator = 480, f"{filtro},scale={LARG}:480:flags=area,format=gray", 1080 / LARG
    else:
        alt = round(s["height"] * LARG / s["width"] / 2) * 2
        vf, fator = f"scale={LARG}:{alt}:flags=area,format=gray", s["width"] / LARG
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-vf", vf, "-f", "rawvideo", "-"], capture_output=True)
    v = np.frombuffer(p.stdout, dtype=np.uint8)
    n = v.size // (LARG * alt)
    return v[: n * LARG * alt].reshape(n, alt, LARG).astype(np.float32), float(num) / float(den), fator


def desloc(a, b, jan):
    A = np.fft.fft2((a - a.mean()) * jan)
    B = np.fft.fft2((b - b.mean()) * jan)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-6
    c = np.real(np.fft.ifft2(R))
    iy, ix = np.unravel_index(np.argmax(c), c.shape)
    H, W = c.shape

    def sub(cm, cz, cp):
        d = cm - 2 * cz + cp
        return 0.0 if abs(d) < 1e-9 else 0.5 * (cm - cp) / d

    dy = iy + sub(c[(iy - 1) % H, ix], c[iy, ix], c[(iy + 1) % H, ix])
    dx = ix + sub(c[iy, (ix - 1) % W], c[iy, ix], c[iy, (ix + 1) % W])
    return (dx - W if dx > W / 2 else dx), (dy - H if dy > H / 2 else dy)


def tremor(arq, janela=None, filtro=None):
    q, fps, fator = quadros(arq, filtro)
    jan = np.outer(np.hanning(q.shape[1]), np.hanning(q.shape[2])).astype(np.float32)
    d = np.array([desloc(q[i], q[i - 1], jan) for i in range(1, len(q))]) * fator
    # tremedeira = a parte rápida da velocidade: velocidade menos a média móvel de ~0,25 s (panorâmica e caminhada
    # suaves ficam na média; a vibração da mão, de 4 a 12 Hz, fica no resto)
    k = max(3, round(0.25 * fps) | 1)
    pad = np.pad(d, ((k // 2, k // 2), (0, 0)), mode="edge")
    media = np.stack([np.convolve(pad[:, j], np.ones(k) / k, mode="valid") for j in range(2)], axis=1)
    resid = np.hypot(*(d - media).T)
    out = {"arquivo": arq, "dur": round(len(q) / fps, 2), "rms": round(float(np.sqrt((resid ** 2).mean())), 2),
           "pico": round(float(resid.max()) if len(resid) else 0.0, 2),
           "movimento": round(float(np.hypot(*d.T).mean()), 2)}
    out["tremido"] = out["rms"] > LIMITE_RMS or out["pico"] > LIMITE_PICO
    if janela:
        n = max(2, round(janela * fps))
        if len(resid) > n:
            m = np.convolve(resid ** 2, np.ones(n) / n, mode="valid")
            pk = np.array([resid[i:i + n].max() for i in range(len(m))])
            custo = np.sqrt(m) + 0.25 * pk  # o pico também pesa: um solavanco isolado aparece
            i0 = int(np.argmin(custo))
            out["melhor"] = [round(i0 / fps, 2), round((i0 + n) / fps, 2), round(float(np.sqrt(m[i0])), 2), round(float(pk[i0]), 2)]
            out["rms_janelas"] = [round(float(x), 2) for x in np.sqrt(m)]
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    janela = None
    if args and args[0] == "--janela":
        janela, args = float(args[1]), args[2:]
    for a in args:
        r = tremor(a, janela)
        print(f"{'TREMIDO' if r['tremido'] else 'ok     '} rms {r['rms']:5.2f} pico {r['pico']:5.2f} mov {r['movimento']:5.2f} px/q"
              f" · {r['dur']:5.2f} s · {a.split('/')[-1]}" + (f" · melhor {r['melhor']}" if 'melhor' in r else ""), flush=True)
