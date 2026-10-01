"""Sincronia voz x boca: movimento na região da boca (Haar + diferença entre quadros) contra o envelope da voz."""
import subprocess, sys, numpy as np, cv2, soundfile as sf
from scipy import signal
import os
VID = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "reel_apresentacao_sem_texto.mp4")
AUD=sys.argv[1]; sr=48000; W,H=540,960
casc=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
x,_=sf.read(AUD,always_2d=True); x=signal.sosfiltfilt(signal.butter(4,[300,3000],'bandpass',fs=sr,output='sos'),x.mean(1))
for t0,t1,nome in [(14.917,19.625,'07 Buenos días'),(30.417,34.958,'12 tapa'),(19.625,22.333,'08 Chegamos')]:
    raw=subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-t",str(t1-t0),"-i",VID,"-vf",f"scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W)
    boxes=[]
    for f in fr:
        fs=casc.detectMultiScale(f,1.1,5,minSize=(80,80))
        boxes.append(max(fs,key=lambda b:b[2]*b[3]) if len(fs) else None)
    ok=[b for b in boxes if b is not None]
    if len(ok)<len(fr)*0.5: print(nome,': rosto detectado em só %d/%d quadros, sem medida'%(len(ok),len(fr))); continue
    mov=[]
    for i in range(1,len(fr)):
        b=boxes[i] if boxes[i] is not None else ok[0]
        fx,fy,fw,fh=b; roi=(slice(fy+int(fh*0.62),fy+int(fh*0.95)),slice(fx+int(fw*0.25),fx+int(fw*0.75)))
        mov.append(np.mean(np.abs(fr[i][roi].astype(float)-fr[i-1][roi].astype(float))))
    mov=np.array(mov)
    n=len(fr); s0=int(t0*sr); J=sr//24
    env=np.array([np.sqrt(np.mean(x[s0+k*J:s0+(k+1)*J]**2)) for k in range(n)])
    denv=np.abs(np.diff(env))
    m=(mov-mov.mean())/mov.std(); a=(denv-denv.mean())/denv.std()
    lags=range(-6,7); c=[np.mean(m[max(0,L):len(m)+min(0,L)]*a[max(0,-L):len(a)-max(0,L)]) for L in lags]
    best=list(lags)[int(np.argmax(c))]
    print('%s: rosto em %d/%d quadros | melhor defasagem %+d quadro(s) (corr %.2f; no 0: %.2f) | positivo = som adiantado'%(nome,len(ok),len(fr),best,max(c),c[6]))
    print('   curva:',' '.join('%+d:%.2f'%(L,v) for L,v in zip(lags,c)))
