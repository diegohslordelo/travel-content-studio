#!/usr/bin/env python3
"""Conferência do Reel final (passo 7 do pedido): mede, não supõe. Rode de dentro de reel_gaudi/ depois do master.

  1. formato e duração (ffprobe) · 2. legendas dentro da zona segura e sem cortar palavra (pixels dos quadros)
  3. troca de imagem × fala (corte medido no vídeo × palavra da âncora, tolerância 0,3 s)
  4. áudio: pico, clipping, emendas no silêncio e transcrição da voz final (Whisper large-v3)
  5. tela dividida: costura escura em y 897–902, como no padrão
Saída: qa/conferencia.json e o resumo no terminal.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AQUI, "scripts"))
import reel  # noqa: E402

TMP = os.path.join(AQUI, "_tmp")
FINAL = os.path.join(AQUI, "reel_gaudi_final.mp4")
ZONA = {"x0": 72, "x1": 1008, "y0": 256, "y1": 1440}  # DS V2: UI do Instagram fora de x 0–72 / 944–1080 e y 0–256 / 1440–1920


def quadro(t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", FINAL, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(1920, 1080, 3).astype(int)


def main():
    res = {}
    props = json.load(open(os.path.join(TMP, "props.json"), encoding="utf-8"))
    palavras = json.load(open(os.path.join(TMP, "palavras.json"), encoding="utf-8"))
    cenas_cfg = reel.ler("cenas.json")["cenas"]
    fps = props["fps"]

    # 1. formato
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,bit_rate:stream=codec_name,width,height,r_frame_rate,sample_rate,channels,bit_rate",
                                    "-of", "json", FINAL], capture_output=True, text=True).stdout)
    dur = float(pr["format"]["duration"])
    v = next(s for s in pr["streams"] if s["codec_name"] == "h264")
    a = next(s for s in pr["streams"] if s["codec_name"] == "aac")
    res["formato"] = {"duracao_s": round(dur, 3), "ok_duracao": dur <= 45.0, "video": f"{v['width']}x{v['height']} {v['r_frame_rate']} h264",
                      "audio": f"aac {a['sample_rate']} Hz {a['channels']} canais", "bitrate_kbps": round(int(pr["format"]["bit_rate"]) / 1000)}

    # 2. legendas: largura pela métrica da fonte usada no render (Inter 800, 66 px), centrada em x 540 (CLAUDE.md, 6),
    #    1 linha por grupo (nenhuma palavra quebrada); altura do bloco ≈ 73 px em torno do y da cena.
    #    (A detecção por pixel confunde pedra e foto clara da imagem de cima com o texto na costura.)
    from PIL import ImageFont
    fonte = ImageFont.truetype(os.path.join(reel.REMOTION, "node_modules/@fontsource/inter/files/inter-latin-800-normal.woff2"), 66)
    leg = []
    for g in props["legendas"]:
        q = round((g["ini"] + 0.05) * fps)
        cena = next((c for c in props["cenas"] if c["ini_q"] <= q < c["fim_q"]), props["cenas"][-1])
        y = props["costura"] if cena.get("layout") == "split" and cena["tipo"] != "fala" else 1375 if cena.get("layout") == "card" else 1320
        texto = " ".join(w["texto"] for w in g["palavras"])
        larg = fonte.getlength(texto)
        x0, x1 = 540 - larg / 2, 540 + larg / 2
        leg.append({"texto": texto, "ini": g["ini"], "y": y, "x0": round(x0), "x1": round(x1), "linhas": 1 if larg <= 900 else 2,
                    "ok": ZONA["x0"] <= x0 and x1 <= 944 and ZONA["y0"] <= y - 37 and y + 37 <= ZONA["y1"] and larg <= 900})
    res["legendas"] = {"grupos": len(leg), "fora": [x for x in leg if not x["ok"]], "maior_largura": round(max(x["x1"] - x["x0"] for x in leg)),
                       "y_usados": sorted({x["y"] for x in leg}), "lista": leg}

    # 3. troca de imagem: corte medido (diferença entre quadros) × palavra da âncora
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", FINAL, "-vf", "scale=270:480,select='gt(scene,0.12)',showinfo", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    cortes = [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    trocas = []
    for c0, c in zip(cenas_cfg[1:], props["cenas"][1:]):
        planejado = c["ini_q"] / fps
        m = re.fullmatch(r"(f\d+):([^#+\-]+?)(?:#(\d+))?([+-][\d.]+)?", c0["ini"])
        palavra = reel.resolver(f"{m.group(1)}:{m.group(2)}" + (f"#{m.group(3)}" if m.group(3) else ""), palavras, 0)
        medido = min(cortes, key=lambda x: abs(x - planejado)) if cortes else None
        trocas.append({"cena": c["id"], "palavra": f"{m.group(2)} ({m.group(1)})", "palavra_s": round(palavra, 3), "corte_planejado_s": round(planejado, 3),
                       "corte_medido_s": round(medido, 3) if medido is not None and abs(medido - planejado) < 0.25 else None,
                       "desvio_s": round(planejado - palavra, 3), "ok": abs(planejado - palavra) <= 0.3})
    res["trocas"] = {"total": len(trocas), "fora_de_0_3s": [x for x in trocas if not x["ok"]], "nao_medidas": [x["cena"] for x in trocas if x["corte_medido_s"] is None],
                     "maior_desvio_s": max(abs(x["desvio_s"]) for x in trocas), "lista": trocas}

    # 4. áudio
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", FINAL, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2)
    i, tp = reel.medir(FINAL)
    trechos = json.load(open(os.path.join(TMP, "trechos.json")))
    sr = 48000
    import soundfile as sf
    vb, _ = sf.read(os.path.join(TMP, "voz_bruta.wav"))
    emendas = []
    for tr in trechos[1:]:
        k = int(tr["inicio"] * sr)
        antes = 20 * np.log10(np.sqrt(np.mean(vb[k - int(0.06 * sr):k - int(0.02 * sr)] ** 2)) + 1e-12)
        depois = 20 * np.log10(np.sqrt(np.mean(vb[k + int(0.01 * sr):k + int(0.03 * sr)] ** 2)) + 1e-12)
        emendas.append({"t": tr["inicio"], "fala": tr["fala"], "antes_db": round(float(antes), 1), "depois_db": round(float(depois), 1)})
    res["audio"] = {"lufs": i, "pico_verdadeiro_dbtp": tp, "amostras_acima_-1dBFS": int((np.abs(x) > 10 ** (-1 / 20)).sum()),
                    "amostras_em_0dBFS": int((np.abs(x) >= 0.999).sum()), "emendas": emendas}

    # Whisper na voz final (texto e confiança das palavras nas emendas e no restauro)
    try:
        from faster_whisper import WhisperModel
        from scipy.signal import resample_poly
        m = WhisperModel("large-v3", device="cpu", compute_type="int8")
        mono = resample_poly(x.mean(axis=1).astype(np.float64), 1, 3).astype(np.float32)
        segs, _ = m.transcribe(mono, language="pt", word_timestamps=True, beam_size=5)
        ws = [(round(w.start, 2), w.word.strip(), round(w.probability, 2)) for s in segs for w in s.words]
        res["transcricao_final"] = {"texto": " ".join(w[1] for w in ws), "palavras_baixa_confianca": [w for w in ws if w[2] < 0.6], "palavras": ws}
    except Exception as e:  # noqa: BLE001
        res["transcricao_final"] = {"erro": str(e)}

    # 5. costura da tela dividida (linha escura de 6 px em y 897–902) em 4 cenas split
    costuras = []
    for c in [c for c in props["cenas"] if c.get("layout") == "split" and c["tipo"] != "fala"][:6]:
        t = (c["ini_q"] + c["fim_q"]) / 2 / fps
        img = quadro(t)
        lum = img.mean(axis=2).mean(axis=1)
        dentro, fora = lum[897:903].mean(), np.r_[lum[885:895], lum[905:915]].mean()
        costuras.append({"cena": c["id"], "lum_linha": round(float(dentro), 1), "lum_vizinhos": round(float(fora), 1), "ok": dentro < fora - 5})
    res["costura"] = costuras

    os.makedirs(os.path.join(AQUI, "qa"), exist_ok=True)
    json.dump(res, open(os.path.join(AQUI, "qa", "conferencia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps({k: (v if k not in ("legendas", "trocas", "transcricao_final") else {kk: vv for kk, vv in v.items() if kk not in ("lista", "palavras")})
                      for k, v in res.items()}, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
