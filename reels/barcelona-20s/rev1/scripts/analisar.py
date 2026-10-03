"""Etapa 1 — métricas automáticas por quadro e por palavra de cada vídeo de Barcelona.

Roda de dentro de reels/barcelona-20s, depois de rev1/scripts/extrair.sh.
Saída: rev1/analise/metricas/<arquivo>.json

Por quadro (proxy a 12 fps, lado maior 1280 px):
  nitidez   variância do Laplaciano (cinza, 640 px de largura)
  luma      média de Y (0–255), % estourado (Y ≥ 250) e % escuro (Y ≤ 8)
  dx, dy    deslocamento global entre quadros (correlação de fase, px no proxy)
  rostos    caixas YuNet (score ≥ 0,8) normalizadas pela altura do quadro
Áudio (WAV 16 kHz mono):
  vad       webrtcvad modo 3, janelas de 30 ms
  palavras  faster-whisper small, timestamps por palavra e probabilidade
Cenas: PySceneDetect ContentDetector (limiar padrão 27).
"""
import json
import os
import sys
import wave

import cv2
import numpy as np
import webrtcvad
from faster_whisper import WhisperModel
from scenedetect import ContentDetector, detect

PROXY = "_tmp/proxy"
WAV = "_tmp/wav"
SAIDA = "rev1/analise/metricas"
YUNET = "_tmp/modelos/yunet.onnx"
os.makedirs(SAIDA, exist_ok=True)


def metricas_video(caminho):
    cap = cv2.VideoCapture(caminho)
    fps = cap.get(cv2.CAP_PROP_FPS)
    det = None
    q = []
    prev = None
    win = None
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        h, w = fr.shape[:2]
        s = 640 / w
        peq = cv2.resize(fr, (640, int(round(h * s))), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(peq, cv2.COLOR_BGR2GRAY)
        y = cv2.cvtColor(fr, cv2.COLOR_BGR2YUV)[:, :, 0]
        gf = g.astype(np.float32)
        if win is None:
            win = cv2.createHanningWindow(gf.shape[::-1], cv2.CV_32F)
        dx = dy = 0.0
        if prev is not None:
            (dx, dy), _ = cv2.phaseCorrelate(prev, gf, win)
            dx, dy = dx / s, dy / s  # em px do proxy
        prev = gf
        if det is None:
            det = cv2.FaceDetectorYN.create(YUNET, "", (peq.shape[1], peq.shape[0]), 0.8)
        _, faces = det.detect(peq)
        rostos = []
        if faces is not None:
            for f in faces:
                x, yy, fw, fh = (float(v) for v in f[:4])
                rostos.append({"cx": round((x + fw / 2) / peq.shape[1], 3),
                               "cy": round((yy + fh / 2) / peq.shape[0], 3),
                               "h": round(fh / peq.shape[0], 3),
                               "score": round(float(f[-1]), 2)})
        q.append({
            "t": round(len(q) / fps, 3),
            "nitidez": round(float(cv2.Laplacian(g, cv2.CV_64F).var()), 1),
            "luma": round(float(y.mean()), 1),
            "estourado": round(float((y >= 250).mean() * 100), 2),
            "escuro": round(float((y <= 8).mean() * 100), 2),
            "dx": round(float(dx), 2), "dy": round(float(dy), 2),
            "rostos": rostos,
        })
    cap.release()
    return fps, w, h, q


def vad(caminho):
    with wave.open(caminho) as wf:
        sr = wf.getframerate()
        pcm = wf.readframes(wf.getnframes())
    v = webrtcvad.Vad(3)
    n = int(sr * 0.03) * 2
    return [1 if v.is_speech(pcm[i:i + n], sr) else 0 for i in range(0, len(pcm) - n + 1, n)]


def main():
    nomes = sorted(os.path.splitext(f)[0] for f in os.listdir(PROXY))
    if len(sys.argv) > 1:
        nomes = sys.argv[1:]
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    for b in nomes:
        fps, w, h, q = metricas_video(f"{PROXY}/{b}.mp4")
        cenas = [(round(a.get_seconds(), 3), round(z.get_seconds(), 3))
                 for a, z in detect(f"{PROXY}/{b}.mp4", ContentDetector())]
        segs, info = modelo.transcribe(f"{WAV}/{b}.wav", word_timestamps=True,
                                       vad_filter=False, condition_on_previous_text=False,
                                       temperature=0.0)
        palavras, segmentos = [], []
        for sg in segs:
            segmentos.append({"ini": round(sg.start, 2), "fim": round(sg.end, 2), "texto": sg.text.strip(),
                              "no_speech_prob": round(sg.no_speech_prob, 3),
                              "avg_logprob": round(sg.avg_logprob, 3)})
            for wd in sg.words or []:
                palavras.append({"ini": round(wd.start, 2), "fim": round(wd.end, 2),
                                 "palavra": wd.word.strip(), "prob": round(wd.probability, 3)})
        json.dump({"arquivo": b, "fps_proxy": fps, "proxy_wh": [w, h], "quadros": q, "cenas": cenas,
                   "vad_30ms": vad(f"{WAV}/{b}.wav"),
                   "whisper": {"idioma": info.language, "prob_idioma": round(info.language_probability, 3),
                               "segmentos": segmentos, "palavras": palavras}},
                  open(f"{SAIDA}/{b}.json", "w"), ensure_ascii=False)
        print(b, len(q), "quadros |", len(palavras), "palavras |", info.language, flush=True)


if __name__ == "__main__":
    main()
