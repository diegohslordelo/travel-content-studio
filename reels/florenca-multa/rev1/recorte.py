"""Recorte do Diego (RobustVideoMatting ResNet50, ONNX) → ../fonte/recorte/<take>.webm (VP9 com alfa, 1080 × 1920). Só o trecho usado de cada tomada."""
import json, os, subprocess, sys, numpy as np, onnxruntime as ort
AQUI=os.path.dirname(os.path.abspath(__file__)); FONTE=os.path.normpath(os.path.join(AQUI,"..","fonte"))
MODELO=os.environ.get("RVM_ONNX","/tmp/claude-0/modelos/rvm_resnet50_fp32.onnx")
d=json.load(open(os.path.join(AQUI,"rev1.json"))); W,H=d["largura"],d["altura"]
so=ort.SessionOptions(); so.intra_op_num_threads=4
s=ort.InferenceSession(MODELO,so,providers=["CPUExecutionProvider"])
alvo=sys.argv[1:] or [t["nome"] for t in d["tomadas"]]
for tk in d["tomadas"]:
    if tk["nome"] not in alvo: continue
    saida=os.path.join(FONTE,"recorte",tk["nome"]+".webm"); os.makedirs(os.path.dirname(saida),exist_ok=True)
    if os.path.exists(saida): print("já existe",saida); continue
    ini=max(0,tk["ini"]-0.5); dur=tk["fim"]+0.3-ini
    dec=subprocess.Popen(["ffmpeg","-v","error","-ss",f"{ini}","-t",f"{dur}","-i",os.path.join(FONTE,tk["arquivo"]),"-vf",f"scale={W}:{H}:flags=lanczos,format=rgb24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgba","-s",f"{W}x{H}","-r","24","-i","-","-c:v","libvpx-vp9","-pix_fmt","yuva420p","-b:v","0","-crf","16","-row-mt","1","-deadline","good","-cpu-used","4","-auto-alt-ref","0",saida],stdin=subprocess.PIPE)
    rec=[np.zeros([1,1,1,1],np.float32)]*4; dr=np.array([0.25],np.float32); n=0
    while True:
        b=dec.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        f=np.frombuffer(b,np.uint8).reshape(H,W,3); x=(f.astype(np.float32)/255).transpose(2,0,1)[None]
        fgr,pha,*rec=s.run(None,{"src":x,"r1i":rec[0],"r2i":rec[1],"r3i":rec[2],"r4i":rec[3],"downsample_ratio":dr})
        a=(np.clip(pha[0,0],0,1)*255).astype(np.uint8); fg=(np.clip(fgr[0].transpose(1,2,0),0,1)*255).astype(np.uint8)
        enc.stdin.write(np.dstack([fg,a]).tobytes()); n+=1
        if n%48==0: print(tk["nome"],n,flush=True)
    enc.stdin.close(); enc.wait(); print(tk["nome"],"ok",n,"quadros (início do arquivo de recorte =",ini,"s do bruto)",flush=True)
