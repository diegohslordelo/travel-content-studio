"""Compara duas versões da mesma voz isolada (original x tratada), alinhadas no tempo."""
import sys, numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal
sr=48000
o,_=sf.read(sys.argv[1],always_2d=True); t,_=sf.read(sys.argv[2],always_2d=True)
n=min(len(o),len(t)); o=o[:n]; t=t[:n]
m=pyln.Meter(sr)
g=m.integrated_loudness(t)-m.integrated_loudness(o)
om,tm=o.mean(1),t.mean(1)*10**(-g/20)   # mesma loudness: só a diferença de forma/timbre
def bp(x,a,b): return signal.sosfiltfilt(signal.butter(4,[a,b],'bandpass',fs=sr,output='sos'),x)
def w(x,J=960): k=len(x)//J*J; return 20*np.log10(np.sqrt((x[:k].reshape(-1,J)**2).mean(1))+1e-10)
ro,rt=w(om),w(tm)
voz=ro>np.percentile(ro,95)-30
print('ganho de loudness aplicado: %+.1f dB'%g)
d=rt-ro
print('variação de nível por janela de 20 ms (voz): p5 %.1f  mediana %.1f  p95 %.1f dB  -> compressão efetiva ~%.1f dB'%(np.percentile(d[voz],5),np.median(d[voz]),np.percentile(d[voz],95),np.percentile(d[voz],95)-np.percentile(d[voz],5)))
# picos x corpo: fator de crista
def crest(x): return 20*np.log10(np.max(np.abs(x))/np.sqrt(np.mean(x**2)))
print('fator de crista: original %.1f dB, tratada %.1f dB'%(crest(om),crest(tm)))
# espectro médio da voz por banda
for a,b in [(60,100),(100,200),(200,350),(350,1000),(1000,2000),(2000,5000),(5000,9000),(9000,16000)]:
    print('  %5d-%5d Hz: %+.1f dB'%(a,b, 20*np.log10(np.sqrt(np.mean(bp(tm,a,b)**2))/np.sqrt(np.mean(bp(om,a,b)**2)))))
# sibilância: janelas sibilantes (5-9k domina 1-4k) e nível do sibilante relativo à voz
so,st=w(bp(om,5000,9000)),w(bp(tm,5000,9000)); po,pt=w(bp(om,1000,4000)),w(bp(tm,1000,4000))
sib=voz&((so-po)>3)
print('janelas sibilantes: %d | sibilante vs mediana da voz: original %.1f dB, tratada %.1f dB'%(sib.sum(), np.median(so[sib])-np.median(ro[voz]), np.median(st[sib])-np.median(rt[voz])))
print('sibilante mais forte: original %.1f, tratada %.1f dB acima da mediana da voz'%(so[sib].max()-np.median(ro[voz]), st[sib].max()-np.median(rt[voz])))
# respirações / pausas: janelas entre -30 e -55 dB abaixo do pico, fora da voz
pa=(~voz)&(ro>np.percentile(ro,5)+6)
if pa.sum():
    print('pausas com respiração/ruído de boca (%d janelas): original %.1f dB abaixo da voz, tratada %.1f dB'%(pa.sum(), np.median(ro[voz])-np.median(ro[pa]), np.median(rt[voz])-np.median(rt[pa])))
print('piso (p5): original %.1f, tratada %.1f dBFS (mesma loudness)'%(np.percentile(ro,5),np.percentile(rt,5)))
