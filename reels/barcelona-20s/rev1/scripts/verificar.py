"""QA de um render: fala no áudio final, loudness, emenda do loop e folha de quadros.

Roda de dentro de reels/barcelona-20s.
  python3 rev1/scripts/verificar.py rev1/previa/previa_sem_marca_540x960.mp4
Saída: <video>.qa.json, <video>.loop.jpg (último × primeiro quadro), <video>.folha.jpg (1 quadro a cada 0,5 s)
"""
import json
import re
import subprocess
import sys

import os

import cv2
import numpy as np
from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps

LATINO = re.compile(r"[A-Za-zÀ-ÿ]")
sys.path.insert(0, os.path.dirname(__file__))
import musica  # noqa: E402


def fala(video):
    a = decode_audio(video, sampling_rate=16000)
    res = {}
    for thr in (0.5, 0.25):
        res[f"silero_{thr}"] = [[round(r["start"] / 16000, 2), round(r["end"] / 16000, 2)]
                                for r in get_speech_timestamps(a, VadOptions(threshold=thr, min_speech_duration_ms=150))]
    m = WhisperModel("small", device="cpu", compute_type="int8")
    reg = res["silero_0.25"]
    for lang in ("pt", "es", "ca", "en"):
        segs, _ = m.transcribe(a, language=lang, word_timestamps=True, vad_filter=False,
                               condition_on_previous_text=False, temperature=0.0)
        ws = [w for s in segs for w in (s.words or [])]
        res[f"whisper_{lang}_todas"] = [(w.word.strip(), round(w.probability, 2), round(w.start, 2)) for w in ws]
        res[f"whisper_{lang}_reconheciveis"] = [
            (w.word.strip(), round(w.probability, 2), round(w.start, 2)) for w in ws
            if w.probability >= 0.5 and LATINO.search(w.word) and any(w.start < r[1] and w.end > r[0] for r in reg)]
    res["fala_detectada"] = any(res[f"whisper_{l}_reconheciveis"] for l in ("pt", "es", "ca", "en"))
    return res


def musica_final(video):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    p = musica.periodicidade(np.frombuffer(raw, np.float32).astype(np.float64))
    seg = [[s, round(float(np.median(p[int(s / 0.032):int((s + 1) / 0.032)])), 2),
            round(float(np.percentile(p[int(s / 0.032):int((s + 1) / 0.032)], 90)), 2)]
           for s in range(int(len(p) * 0.032))]
    return {"mediana": round(float(np.median(p)), 3), "p90": round(float(np.percentile(p, 90)), 3),
            "trechos_musicais": musica.trechos(p), "por_segundo_med_p90": seg}


def loudness(video):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    resumo = out[out.rfind("Summary"):]
    num = lambda k: float(re.search(k + r":\s+(-?[\d.]+)", resumo).group(1))
    return {"I_lufs": num("I"), "LRA_lu": num("LRA"), "true_peak_dbtp": num("Peak")}


def quadros(video):
    cap = cv2.VideoCapture(video)
    fs = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        fs.append(f)
    return fs, cap.get(cv2.CAP_PROP_FPS)


def main():
    v = sys.argv[1]
    fs, fps = quadros(v)
    a, z = fs[0], fs[-1]
    ha = cv2.calcHist([cv2.cvtColor(a, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    hz = cv2.calcHist([cv2.cvtColor(z, cv2.COLOR_BGR2HSV)], [0, 1, 2], None, [16, 8, 8], [0, 180, 0, 256, 0, 256])
    ya, yz = (cv2.cvtColor(x, cv2.COLOR_BGR2GRAY).astype(float) for x in (a, z))
    loop = {"correl_hist_hsv": round(float(cv2.compareHist(cv2.normalize(ha, ha), cv2.normalize(hz, hz),
                                                           cv2.HISTCMP_CORREL)), 3),
            "luma_ultimo": round(yz.mean(), 1), "luma_primeiro": round(ya.mean(), 1),
            "ceu_topo_ultimo_pct": round(float((cv2.cvtColor(z, cv2.COLOR_BGR2HSV)[: z.shape[0] // 3, :, 0]
                                                 .astype(int) - 105).__abs__().__lt__(15).mean() * 100), 1),
            "ceu_topo_primeiro_pct": round(float((cv2.cvtColor(a, cv2.COLOR_BGR2HSV)[: a.shape[0] // 3, :, 0]
                                                   .astype(int) - 105).__abs__().__lt__(15).mean() * 100), 1)}
    h = 640
    par = np.hstack([cv2.resize(z, (h * 9 // 16, h)), np.full((h, 8, 3), 255, np.uint8), cv2.resize(a, (h * 9 // 16, h))])
    cv2.putText(par, "ultimo", (8, 24), 0, 0.7, (255, 255, 255), 2)
    cv2.putText(par, "primeiro", (h * 9 // 16 + 16, 24), 0, 0.7, (255, 255, 255), 2)
    cv2.imwrite(v + ".loop.jpg", par)
    passo = int(round(fps / 2))
    mini = [cv2.resize(f, (135, 240)) for f in fs[::passo]]
    for i, m in enumerate(mini):
        cv2.putText(m, f"{i * passo / fps:.1f}s", (4, 16), 0, 0.45, (255, 255, 255), 1)
    while len(mini) % 11:
        mini.append(np.zeros_like(mini[0]))
    cv2.imwrite(v + ".folha.jpg", np.vstack([np.hstack(mini[i:i + 11]) for i in range(0, len(mini), 11)]))
    qa = {"video": v, "quadros": len(fs), "fps": fps, "loop": loop, "loudness": loudness(v), "musica": musica_final(v), "fala": fala(v)}
    json.dump(qa, open(v + ".qa.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: qa[k] for k in ("quadros", "fps", "loop", "loudness")}, ensure_ascii=False))
    print("música:", {k: v for k, v in qa["musica"].items() if k != "por_segundo_med_p90"})
    print("silero:", qa["fala"]["silero_0.5"], qa["fala"]["silero_0.25"])
    for l in ("pt", "es", "ca", "en"):
        print(l, "todas:", qa["fala"][f"whisper_{l}_todas"][:12], "| reconhecíveis:", qa["fala"][f"whisper_{l}_reconheciveis"])
    print("FALA DETECTADA" if qa["fala"]["fala_detectada"] else "sem fala reconhecível")


if __name__ == "__main__":
    main()
