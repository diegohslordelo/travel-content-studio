"""Tratamento de áudio da REV1 (AUDIO_REVIEW_STANDARD v1.1.0, seção 7.3): cadeia única, sempre a partir do original.

Uso (de dentro de youtube/barcelona/):
  python3 rev1/audio/scripts/tratar.py ORIGINAL.mov|flac SAIDA.m4a RELATORIO.json
Cadeia (rev1/audio/cadeia_audio.json):
  1. decodifica a faixa do original (float, 44,1 kHz, estéreo)
  2. nível 2: ganho por trecho com rampas (inserções de música −6 dB; falas muito baixas +5 a +6,5 dB)
  3. nível 8: ganho global G (ajustado em até 3 passes para −14 LUFS no exportado) → sobreamostragem 4× →
     alimiter (teto −1,5 dBFS, 5/80 ms, sem ganho automático) → 48 kHz → AAC 192 kbps
  4. mede o exportado: LUFS integrado, pico verdadeiro, amostras no teto, redução do limitador
"""
import json, os, re, subprocess, sys
import numpy as np

orig, saida, rel = sys.argv[1:4]
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(AQUI, "cadeia_audio.json"), encoding="utf-8"))
SR = 44100
TMP = os.path.join(os.path.dirname(AQUI), "_tmp")
os.makedirs(TMP, exist_ok=True)

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", orig, "-map", "0:a", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
n = len(x)

# --- nível 2: envelope de ganho (dB) com rampas dentro de cada trecho
env = np.zeros(n)
for s in C["nivel_2_ganho_por_trecho"]:
    a, b = int(s["inicio"] * SR), min(int(s["fim"] * SR), n)
    r = int((C["rampa_ms"] if s["id"].startswith("P01") else C["rampa_em_corte_ms"]) / 1000 * SR)
    g = np.full(b - a, s["ganho_db"])
    rr = min(r, (b - a) // 2)
    if rr:
        g[:rr] *= np.linspace(0, 1, rr)
        if b < n:
            g[-rr:] *= np.linspace(1, 0, rr)
    env[a:b] = g
y = x * (10 ** (env / 20))[:, None]
wav = os.path.join(TMP, "audio_nivel2.f32")
y.astype(np.float32).tofile(wav)


def ebur(arq):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", arq, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
    lra = float(re.findall(r"LRA:\s+(-?[\d.]+) LU", e)[-1])
    return i, tp, lra


def exportar(G):
    lim = 10 ** (C["nivel_8"]["teto_limitador_dbfs"] / 20)
    lat = int(round(0.005 * SR * 4))   # latência do alimiter = attack (5 ms), compensada para não atrasar o áudio
    af = (f"volume={G:.3f}dB,aresample={SR * 4},apad=pad_len={lat},"
          f"alimiter=limit={lim:.5f}:attack=5:release=80:level=0:level_in=1:level_out=1,"
          f"atrim=start_sample={lat},asetpts=PTS-STARTPTS,aresample=48000")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav, "-af", af,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", saida], check=True)
    return af


i0, tp0, _ = ebur(orig)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav, os.path.join(TMP, "n2.flac")], check=True)
i2, tp2, _ = ebur(os.path.join(TMP, "n2.flac"))
G = -14.0 - i2
passes = []
# critério: o primeiro G dentro da tolerância [PROJETO] (−14 ± 1 LU) com pico verdadeiro ≤ −1 dBTP no exportado;
# se o pico estoura, o ganho desce (não se empurra o limitador para cumprir o loudness)
for k in range(6):
    af = exportar(G)
    i, tp, lra = ebur(saida)
    passes.append({"G_db": round(G, 2), "I": i, "TP": tp})
    if tp > -1.0:
        G -= max(0.3, tp + 1.0)
        continue
    if -15.0 < i < -13.0:
        break
    G += -14.0 - i
# --- redução do limitador: compara o sinal com ganho (antes do limitador) e o exportado, por janela de 100 ms
dec = subprocess.run(["ffmpeg", "-v", "error", "-i", saida, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
z = np.frombuffer(dec, np.float32).reshape(-1, 2).astype(np.float64)
m = min(len(z), n)
w = int(0.1 * SR)
k = m // w
pre = np.abs(y[:k * w] * 10 ** (G / 20)).max(axis=1).reshape(k, w).max(axis=1)
pos = np.abs(z[:k * w]).max(axis=1).reshape(k, w).max(axis=1)
teto_lin = 10 ** (C["nivel_8"]["teto_limitador_dbfs"] / 20)
a0, b0 = y[int(100 * SR):int(105 * SR), 0] * 10 ** (G / 20), z[int(100 * SR):int(105 * SR) + 3000, 0]
atraso = int(np.argmax(np.correlate(b0[:len(a0) + 2000], a0, "valid")))
red = np.where(pre > teto_lin, 20 * np.log10(np.maximum(pre, 1e-9) / np.maximum(pos, 1e-9)), 0)
red = np.clip(red, 0, None)
tc = lambda s: f"{int(s // 60):02d}:{s % 60:05.2f}"  # noqa: E731
top = np.argsort(-red)[:12]
teto = int((np.abs(z) >= 0.999).sum())
pr = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate,duration",
                     "-of", "json", saida], capture_output=True, text=True).stdout
out = {
    "original": {"I_LUFS": i0, "TP_dBTP": tp0},
    "apos_nivel_2": {"I_LUFS": i2, "TP_dBTP": tp2},
    "passes_nivel_8": passes,
    "exportado": {"arquivo": os.path.basename(saida), "I_LUFS": i, "TP_dBTP": tp, "LRA_LU": lra, "amostras_no_teto": teto,
                  "desvio_LU": round(i + 14.0, 2), "ffprobe": json.loads(pr)["streams"][0]},
    "limitador": {"atraso_residual_amostras": atraso, "janelas_100ms_com_reducao": int((red > 0.1).sum()), "acima_1dB": int((red > 1).sum()),
                  "acima_2dB": int((red > 2).sum()), "acima_3dB": int((red > 3).sum()), "max_dB": round(float(red.max()), 2),
                  "fracao_do_tempo_%": round(100 * float((red > 0.1).mean()), 2),
                  "maiores": [{"t": tc(j * 0.1), "dB": round(float(red[j]), 2)} for j in top]},
    "cadeia_ffmpeg_nivel_8": af,
}
json.dump(out, open(rel, "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
