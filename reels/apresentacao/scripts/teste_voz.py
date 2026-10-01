"""teste_voz.mp4: só os trechos com voz (narração na apresentação e as falas da montagem), já tratados e mixados
como no Reel (áudio final, -14 LUFS / -1 dBTP), com a imagem de cada trecho em 540x960 e o LUFS medido.

Uso: python3 teste_voz.py lista_de_cortes.json   (roda antes a etapa de áudio do render)
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R  # noqa: E402

edl = R.carregar(sys.argv[1])
tmp = edl["_tmp"]
R.etapa_audio(edl)
final = os.path.join(tmp, "audio_final.wav")
cortes = edl["_cortes"]
nar = edl["narracao"]
off = float(nar["inicio"]) - float(nar["corte_tomada"][0])
trechos = []
a, z = edl["_blocos"]["apresentacao"]
trechos.append(("Narração (com o som das cenas por baixo)", a, z, [c for c in cortes if c["bloco"] == "apresentacao"],
                (nar["voz_trecho"][0] + off, nar["voz_trecho"][1] + off)))
for c in cortes:
    if c.get("fala"):
        fa, fb = c["fala_trecho"]
        texto = " ".join(l["texto"].replace("*", "") for l in c.get("legendas", []))
        trechos.append((f"{c.get('cidade')}: {texto}", c["ini"], c["fim"], [c],
                        (c["ini"] + fa - c["entrada"], c["ini"] + fb - c["entrada"])))
fonte = os.path.join(R.FONTES, "Montserrat-SemiBold.ttf")
partes, linhas = [], []
for k, (nome, a, z, cs, (va, vb)) in enumerate(trechos):
    vids = []
    for c in cs:
        v = os.path.join(tmp, f"tv_{k}_{c['f0']}.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['entrada']:.3f}", "-i", c["_arq"], "-map", "0:v:0",
                        "-vf", f"{R.filtro_video(c)},fps=24,scale=540:960,setsar=1", "-frames:v", str(c["frames"]),
                        "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-an", v], check=True)
        vids.append(v)
    lista = os.path.join(tmp, f"tv_{k}.txt")
    open(lista, "w").write("".join(f"file '{v}'\n" for v in vids))
    rot = nome.replace(":", "\\:").replace("'", "")
    parte = os.path.join(tmp, f"tv_parte_{k}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-ss", f"{a:.3f}", "-t", f"{z - a:.3f}",
                    "-i", final, "-filter_complex",
                    f"[0:v]setpts=N/(24*TB),drawbox=x=0:y=40:w=iw:h=86:color=black@0.55:t=fill,"
                    f"drawtext=fontfile={fonte}:text='{rot}':fontcolor=white:fontsize=20:x=16:y=52:line_spacing=6[v];"
                    f"[1:a]apad=pad_dur=0.4[a]", "-map", "[v]", "-map", "[a]", "-t", f"{z - a + 0.4:.3f}",
                    "-c:v", "libx264", "-crf", "22", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", parte],
                   check=True)
    partes.append(parte)
    voz = R.medir_loudness(final, va, vb)["I"]
    linhas.append((nome, a, z, voz))
lista = os.path.join(tmp, "tv_partes.txt")
open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
saida = os.path.join(edl["_base"], "teste_voz.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-movflags", "+faststart", saida], check=True)
total = R.medir_loudness(saida)
rel = json.load(open(os.path.join(tmp, "audio_relatorio.json")))
with open(os.path.join(edl["_base"], "teste_voz_lufs.txt"), "w") as f:
    f.write("teste_voz.mp4 · loudness medido (EBU R128)\n\n")
    f.write("Antes da normalização final (cada voz tratada separadamente):\n")
    for c in rel["cortes"]:
        if c.get("tipo") in ("fala", "narracao"):
            f.write(f"  {str(c['corte']):>9}: {c['lufs_fala']:.1f} LUFS (bruto {c['lufs_bruto']:.1f}; redução de ruído com piso {c['piso_db']:.0f} dB)\n")
    f.write("\nNo áudio final do Reel (-14 LUFS no total), só nos trechos de voz:\n")
    for nome, a, z, voz in linhas:
        f.write(f"  {a:6.2f}-{z:6.2f} s  {voz:6.1f} LUFS  {nome}\n")
    f.write(f"\nteste_voz.mp4 inteiro: {total['I']:.1f} LUFS integrados, pico {total['TP']:.1f} dBTP\n")
    f.write(f"Reel inteiro (áudio final): {rel['final']['I']:.1f} LUFS integrados, pico {rel['final']['TP']:.1f} dBTP\n")
print(open(os.path.join(edl["_base"], "teste_voz_lufs.txt")).read())
