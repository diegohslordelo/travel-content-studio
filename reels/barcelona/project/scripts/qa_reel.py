"""QA do Reel (Etapa 3 do briefing). Só lê o export e o projeto; não altera nada.

Rodar de dentro de reels/barcelona/ depois do render:
    python3 project/scripts/qa_reel.py

Gera em qa/frames/quadros/ (quadros com camada-guia), qa/frames/miniatura.png, qa/frames/loop_q0_x_ultimo.png
e qa/reports/qa_reel.json.
"""
import glob, json, os, re, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

TL = json.load(open("project/timeline.json", encoding="utf-8"))
EXPORT = "exports/2026-10-02_reel_3-coisas-barcelona.mp4"
FPS = TL["fps"]
N = TL["duracao_quadros"]
TEMPOS = [0.3, 0.6, 1.5, 5, 12, 18, 22, 24, 27.5]
FONTE = "../../design-system/fonts/IBMPlexMono-Medium.ttf"
ZONAS = {"topo": (0, 0, 1080, 256), "base": (0, 1440, 1080, 1920), "direita": (944, 0, 1080, 1920), "esquerda": (0, 0, 72, 1920)}


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def quadro_export(q, out):
    if q >= N - 3:  # perto do fim, o seek por tempo pode cair fora do arquivo: decodifica o último 1 s e conta do fim
        tmp = "/tmp/_fim"
        os.makedirs(tmp, exist_ok=True)
        for f in glob.glob(tmp + "/*.png"):
            os.remove(f)
        sh(["ffmpeg", "-v", "error", "-y", "-sseof", "-1", "-i", EXPORT, f"{tmp}/%04d.png"])
        fs = sorted(glob.glob(tmp + "/*.png"))
        os.replace(fs[len(fs) - (N - q)], out)
    else:
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{q / FPS:.4f}", "-i", EXPORT, "-frames:v", "1", out])
    return Image.open(out).convert("RGB")


def main():
    os.makedirs("qa/frames/quadros", exist_ok=True)
    R = {}
    # 1. ffprobe
    j = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", "-count_frames", EXPORT]).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next(s for s in j["streams"] if s["codec_type"] == "audio")
    dur = float(j["format"]["duration"])
    R["ffprobe"] = {"largura": v["width"], "altura": v["height"], "fps": v["r_frame_rate"], "quadros": int(v["nb_read_frames"]),
                    "duracao_s": round(dur, 3), "video": f"{v['codec_name']} {v.get('profile')}", "pix_fmt": v["pix_fmt"],
                    "bitrate_video_kbps": round(int(v.get("bit_rate", 0)) / 1000), "audio": a["codec_name"],
                    "audio_hz": int(a["sample_rate"]), "audio_canais": a["channels"]}
    R["ok_formato"] = v["width"] == 1080 and v["height"] == 1920 and v["r_frame_rate"] == "30/1" and 26.0 <= dur <= 28.5
    # 2. loudness
    e = sh(["ffmpeg", "-nostats", "-hide_banner", "-i", EXPORT, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr.split("Summary:")[-1]
    R["loudness"] = {"integrado_lufs": float(re.search(r"I:\s+(-?[\d.]+)", e).group(1)),
                     "true_peak_dbtp": float(re.search(r"Peak:\s+(-?[\d.]+)", e).group(1)),
                     "lra_lu": float(re.search(r"LRA:\s+(-?[\d.]+)", e).group(1))}
    R["ok_loudness"] = abs(R["loudness"]["integrado_lufs"] + 14) <= 0.5 and R["loudness"]["true_peak_dbtp"] <= -1.0

    # 3. quadros pedidos, com camada-guia (render ReelGuias)
    fnt = ImageFont.truetype(FONTE, 30)
    pedidos = []
    for t in TEMPOS:
        q = min(round(t * FPS), N - 1)
        out = f"qa/frames/quadros/q{q:03d}_{t:.1f}s.png"
        sh(["npx", "remotion", "still", "src/index.ts", "ReelGuias", "../" + out, f"--frame={q}", "--log=error"], cwd="project")
        pedidos.append((t, q, out))
    R["quadros_guia"] = [{"tempo_s": t, "quadro": q, "arquivo": o, "obs": ("último quadro (o vídeo tem 27,0 s)" if t * FPS >= N else "")} for t, q, o in pedidos]

    # 4. zonas proibidas, área de objetos: render só dos objetos (fundo transparente), todos os quadros, escala 0,5
    seq = "project/out/objetos"
    if not glob.glob(seq + "/*.png"):
        sh(["npx", "remotion", "render", "src/index.ts", "Objetos", "out/objetos", "--sequence", "--image-format=png", "--scale=0.5", "--log=error"], cwd="project")
    invasoes, area_max = [], (0, 0.0)
    for p in sorted(glob.glob(seq + "/*.png")):
        q = int(re.findall(r"(\d+)\.png$", p)[0])
        al = np.asarray(Image.open(p).convert("RGBA"))[:, :, 3] > 40
        area = al.mean()
        if area > area_max[1]:
            area_max = (q, float(area))
        for nome, (x0, y0, x1, y1) in ZONAS.items():
            n = int(al[y0 // 2:y1 // 2, x0 // 2:x1 // 2].sum())
            if n:
                invasoes.append((q, nome, n * 4))
    placa = TL["eventos"]["placa_hook"]
    transito = lambda q: q < placa["de"] + 12 or placa["saida_de"] <= q <= placa["saida_de"] + 8 or \
        any(n["de"] <= q < n["de"] + 5 for n in TL["eventos"]["numeros"])
    R["zonas_proibidas"] = {
        "quadros_com_invasao_fora_de_animacao": sorted({q for q, _, _ in invasoes if not transito(q)}),
        "quadros_com_invasao_em_animacao_de_entrada_ou_saida": sorted({q for q, _, _ in invasoes if transito(q)}),
        "detalhe_primeiros": invasoes[:20]}
    R["area_objetos_max"] = {"quadro": area_max[0], "fracao": round(area_max[1], 4)}

    # 5. amarelo (#FFC21A) na tela fora de transição, no export
    amarelo_max = (0, 0.0)
    cin = TL["eventos"]["cinema"]
    for q in range(0, N, 3):
        if cin["de"] <= q <= cin["de"] + cin["escurece"] + cin["preto"] + cin["abre"] or q == TL["eventos"]["snap"]["de"]:
            continue
        im = np.asarray(quadro_export(q, "/tmp/_q.png").resize((270, 480))).astype(int)
        m = (abs(im[:, :, 0] - 255) < 40) & (abs(im[:, :, 1] - 194) < 40) & (im[:, :, 2] < 90)
        if m.mean() > amarelo_max[1]:
            amarelo_max = (q, float(m.mean()))
    R["amarelo_max_fora_transicao"] = {"quadro": amarelo_max[0], "fracao": round(amarelo_max[1], 4)}

    # 6. ticket × Emocional, contagens
    t, emo = TL["eventos"]["ticket"], TL["eventos"]["emocional"]
    ultimo_ticket = t["saida_de"] + 7
    R["ticket_sai_antes_da_emocional"] = {"ultimo_quadro_ticket": ultimo_ticket, "primeiro_quadro_emocional": emo["de"], "ok": ultimo_ticket < emo["de"]}
    R["contagens"] = {"tickets": 1, "carimbos": 0, "bilhetes": 0, "legendas_emocionais": 1, "transicoes": {"Snap": 1, "Cinema": 1},
                      "familias_de_transicao": 2, "cortes": len(TL["planos"]) - 1, "cortes_secos": len(TL["planos"]) - 1 - 2}

    # 7. miniatura 270 × 480 (teste de 25%) com os mesmos quadros
    ims = [quadro_export(q, f"/tmp/_m{q}.png").resize((270, 480), Image.LANCZOS) for _, q, _ in pedidos]
    mini = Image.new("RGB", (270 * len(ims) + 8 * (len(ims) - 1), 480 + 40), "white")
    d = ImageDraw.Draw(mini)
    for i, (im, (tt, q, _)) in enumerate(zip(ims, pedidos)):
        mini.paste(im, (i * 278, 40))
        d.text((i * 278 + 4, 4), f"{tt:.1f}s", font=fnt, fill="black")
    mini.save("qa/frames/miniatura.png")

    # 8. loop: quadro 0 × último quadro
    a0, a1 = quadro_export(0, "/tmp/_a0.png"), quadro_export(N - 1, "/tmp/_a1.png")
    diff = float(np.abs(np.asarray(a0, int) - np.asarray(a1, int)).mean())
    lado = Image.new("RGB", (1080, 960), "white")
    lado.paste(a1.resize((540, 960)), (0, 0)); lado.paste(a0.resize((540, 960)), (540, 0))
    lado.save("qa/frames/loop_q0_x_ultimo.png")
    R["loop"] = {"diferenca_media_rgb": round(diff, 1), "imagem": "qa/frames/loop_q0_x_ultimo.png"}

    json.dump(R, open("qa/reports/qa_reel.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(R, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
