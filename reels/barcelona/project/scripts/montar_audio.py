"""Monta a trilha de áudio do Reel (voz + ambiente real sob a Cinema), sem música.

Rodar de dentro de reels/barcelona/:
    python3 project/scripts/montar_audio.py

1. Voz: cada bloco de narration/ é cortado (entrada/saída do timeline), recebe corte de graves em 80 Hz e
   é posicionado no tempo do Reel.
2. Ambiente: som real do IMG_1152 (interior da Sagrada Família) sob a transição Cinema, 6 dB abaixo da voz
   (DS V2, Som), com fade de 80 ms nas pontas.
3. Mix: loudnorm em 2 passadas para −14 LUFS integrado e true peak de −1,5 dBTP (margem para o encode AAC);
   depois mede com ebur128. Alvo do briefing: −14 LUFS e pico real ≤ −1 dBTP.
Saída: project/out/audio_mix.wav (48 kHz, estéreo, 24 bits). Não altera os arquivos de narração.
"""
import json, os, re, subprocess

TL = json.load(open("project/timeline.json", encoding="utf-8"))
OUT = "project/out"
DUR = TL["duracao_quadros"] / TL["fps"]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def lufs(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    s = r.stderr.split("Summary:")[-1]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))
    return i, tp


def main():
    os.makedirs(OUT, exist_ok=True)
    ins, filt, mix = [], [], []
    for k, v in enumerate(TL["voz"]):
        ins += ["-i", os.path.join("narration", v["arquivo"])]
        d = v["saida_s"] - v["entrada_s"]
        ms = int(round(v["reel_s"] * 1000))
        filt.append(f"[{k}:a]atrim={v['entrada_s']}:{v['saida_s']},asetpts=PTS-STARTPTS,aresample=48000,"
                    f"aformat=channel_layouts=stereo,highpass=f=80,afade=t=in:d=0.01,afade=t=out:st={d - 0.03:.3f}:d=0.03,"
                    f"adelay={ms}|{ms}[v{k}]")
        mix.append(f"[v{k}]")
    voz_only = os.path.join(OUT, "_voz.wav")
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
         ";".join(filt) + f";{''.join(mix)}amix=inputs={len(mix)}:normalize=0,apad=whole_dur={DUR}",
         "-t", f"{DUR}", "-c:a", "pcm_s24le", voz_only])
    voz_i, _ = lufs(voz_only)

    a = TL["ambiente_cinema"]
    amb_src = os.path.join(OUT, "_amb_src.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join("footage", a["arquivo"]), "-map", "0:a:0", "-ac", "2",
         "-ar", "48000", "-c:a", "pcm_s24le", amb_src])
    amb_i, _ = lufs(amb_src)  # nível do som do lugar no clipe inteiro
    ganho = (voz_i + a["rel_voz_db"]) - amb_i
    ms = int(round(a["reel_s"] * 1000))
    d = a["duracao_s"]
    mix_pre = os.path.join(OUT, "_mix_pre.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", voz_only, "-i", amb_src, "-filter_complex",
         f"[1:a]atrim={a['entrada_s']}:{a['entrada_s'] + d},asetpts=PTS-STARTPTS,volume={ganho:.2f}dB,"
         f"afade=t=in:d=0.08,afade=t=out:st={d - 0.08:.3f}:d=0.08,adelay={ms}|{ms}[amb];"
         f"[0:a][amb]amix=inputs=2:normalize=0,atrim=0:{DUR}",
         "-c:a", "pcm_s24le", mix_pre])

    # loudnorm 2 passadas
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mix_pre, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex("{"):])
    final = os.path.join(OUT, "audio_mix.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", mix_pre, "-af",
         f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
         f"aresample=48000", "-ar", "48000", "-c:a", "pcm_s24le", final])
    i, tp = lufs(final)
    rel = {"voz_lufs_antes": voz_i, "ambiente_lufs_clipe": amb_i, "ganho_ambiente_db": round(ganho, 2),
           "loudnorm_medido": m, "final_lufs": i, "final_true_peak_dbtp": tp}
    json.dump(rel, open(os.path.join(OUT, "audio_relatorio.json"), "w"), indent=1)
    print(json.dumps({k: rel[k] for k in rel if k != "loudnorm_medido"}, indent=1))


if __name__ == "__main__":
    main()
