"""Decupagem: corta a voz e o vídeo do Diego nos mesmos trechos (quadros inteiros a 30 qps).
Roda de dentro de reels/gta6-cidades/rev1."""
import json, subprocess, numpy as np, soundfile as sf, os
E = json.load(open("edicao.json"))
FPS = E["fps"]; os.makedirs("build", exist_ok=True)
def q(t): return round(t * FPS) / FPS
partes = []; linha = []; t = 0.0
for f in E["falas"]:
    a, b = q(f["entrada"]), q(f["saida"])
    x, sr = sf.read(f"../_tmp/wav48/{f['arquivo']}.wav", dtype="float32")
    seg = x[int(round(a*sr)):int(round(b*sr))].copy()
    n = int(sr*E["audio"]["fade_ms"]/1000); r = np.linspace(0,1,n)
    seg[:n] *= r; seg[-n:] *= r[::-1]
    partes.append(seg)
    linha.append({**f, "entrada_q": a, "saida_q": b, "inicio": round(t,4), "fim": round(t+b-a,4)})
    t += b - a
voz = np.concatenate(partes)
sf.write("build/voz_crua.wav", voz, sr, subtype="PCM_24")
subprocess.run(["ffmpeg","-v","error","-y","-i","build/voz_crua.wav","-af",
  f"highpass=f={E['audio']['passa_alta_hz']},afftdn={E['audio']['afftdn']}","-c:a","pcm_s24le","build/voz.wav"],check=True)
json.dump({"duracao": round(t,4), "falas": linha}, open("build/linha_voz.json","w"), ensure_ascii=False, indent=1)
# vídeo do Diego: mesmos trechos, HDR->SDR, 1080x1920, 30 qps, sem áudio
ins=[]; filt=[]
for i,f in enumerate(linha):
    ins += ["-ss", f"{f['entrada_q']:.4f}", "-t", f"{f['saida_q']-f['entrada_q']:.4f}", "-i", f"../fonte/fala/{f['arquivo']}.MOV"]
    filt.append(f"[{i}:v]zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,fps={FPS},setpts=PTS-STARTPTS,trim=duration={f['saida_q']-f['entrada_q']:.4f}[v{i}]")
filt.append("".join(f"[v{i}]" for i in range(len(linha))) + f"concat=n={len(linha)}:v=1:a=0[out]")
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(filt),"-map","[out]","-c:v","libx264","-crf","16","-preset","medium","-pix_fmt","yuv420p","build/diego.mp4"],check=True)
print("voz", round(t,3), "s")
