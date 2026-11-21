import json, librosa, numpy as np, os
P="fonte/musica"; out={}
for f in sorted(os.listdir(P)):
    if not f.endswith('.mp3'): continue
    y,sr=librosa.load(f"{P}/{f}",sr=22050,mono=True,offset=5,duration=90)
    H,Pc=librosa.effects.hpss(y)
    perc=float(np.sum(Pc**2)/(np.sum(H**2)+np.sum(Pc**2)))
    oenv=librosa.onset.onset_strength(y=y,sr=sr)
    tg=librosa.feature.tempogram(onset_envelope=oenv,sr=sr)
    bpms=librosa.tempo_frequencies(tg.shape[0],sr=sr)
    m=tg.mean(axis=1); ok=(bpms>=70)&(bpms<=200)
    t1=float(bpms[ok][np.argmax(m[ok])])
    pulso=float(librosa.beat.plp(onset_envelope=oenv,sr=sr).mean())
    flux=float(oenv.mean())
    rate=len(librosa.onset.onset_detect(onset_envelope=oenv,sr=sr))/90
    out[f[:-4]]={"bpm_tempograma":round(t1,1),"percussao":round(perc,3),"ataques_s":round(rate,2),"fluxo":round(flux,3),"pulso":round(pulso,3)}
# índice de animação: normaliza e soma
ks=["bpm_tempograma","percussao","ataques_s","fluxo","pulso"]
arr={k:np.array([out[n][k] for n in out]) for k in ks}
for n in out:
    out[n]["animacao"]=round(float(sum((out[n][k]-arr[k].mean())/arr[k].std() for k in ks)/len(ks)),2)
for n,v in sorted(out.items(),key=lambda x:-x[1]["animacao"]):
    print(f"{v['animacao']:5.2f}  {n:<52} bpm {v['bpm_tempograma']:6.1f} perc {v['percussao']:.2f} ataques {v['ataques_s']:4.2f} fluxo {v['fluxo']:.2f} pulso {v['pulso']:.2f}")
json.dump(out,open('_tmp/animacao.json','w'),ensure_ascii=False,indent=1)
