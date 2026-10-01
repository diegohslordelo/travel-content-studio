"""Tabelas de diagnóstico (antes) e verificação (depois) em Markdown."""
import json, numpy as np, soundfile as sf
from scipy import signal
a=json.load(open('diag_rev5.json')); b=json.load(open('verif_v6.json')); n=json.load(open('diag_nar_orig.json'))['narracao']
sr=48000
def f(v,d=1): return '—' if v is None or (isinstance(v,float) and np.isnan(v)) else ('%.*f'%(d,v)).replace('.',',')
def origem(o):
    if not o: return '—'
    fr={'grave < 200 Hz':o['<200Hz'],'médios 200 Hz-2 kHz':o['200-2k'],'agudos 2-8 kHz':o['2k-8k']}
    k=max(fr,key=fr.get); return '%s (%d%%)'%(k,round(100*fr[k]))
def mono(arq,t0,t1):
    x,_=sf.read(arq,always_2d=True); s=x[int(t0*sr):int(t1*sr)]
    sos=signal.butter(4,[300,3000],'bandpass',fs=sr,output='sos')
    st=np.sqrt(np.mean((signal.sosfiltfilt(sos,s[:,0])**2+signal.sosfiltfilt(sos,s[:,1])**2)/2)); mo=np.sqrt(np.mean(signal.sosfiltfilt(sos,s.mean(1))**2))
    return 20*np.log10(mo/st)
cenas=[k for k in a if k!='REEL INTEIRO']
tempos=[(0,3),(3,4.25),(4.25,8.458),(8.458,10.75),(10.75,12.375),(12.375,14.917),(14.917,19.625),(19.625,22.333),(22.333,24.917),(24.917,27.417),(27.417,30.417),(30.417,34.958),(34.958,41.417)]
print('| Medida | Valor |\n|---|---|')
print('| Piso de ruído | %s dBFS (%s; gravação limpa) |'%(f(n['piso_ruido_dBFS']),origem(n['origem_ruido'])))
print('| LUFS integrado / curto prazo (mín–máx) | %s / %s a %s |'%(f(n['LUFS_I']),f(n['ST_min']),f(n['ST_max'])))
print('| Pico verdadeiro | %s dBTP |'%f(n['TP_dBTP']))
print('| Clipping / trechos achatados | %d / %d |'%(n['clip_amostras'],n['achatados']))
print('| DC offset | 0 |')
print('| Correlação L/R | %s (estéreo do celular, sem inversão de fase nem mono falso) |'%f(n['corr_LR'],2))
print('\n#TABELA2\n')
print('| Cena | Piso de ruído (dBFS) | Origem do ruído | LUFS da voz | LUFS fora da voz | Curto prazo, mediana (LUFS) | Pico verdadeiro (dBTP) | Agudos 4–12 kHz vs 0,3–4 kHz (dB) | Perda da voz em mono (dB) |')
print('|---|---|---|---|---|---|---|---|---|')
for k,(t0,t1) in zip(cenas,tempos):
    x,y=a[k],b[k]
    print('| %s | %s → %s | %s | %s → %s | %s → %s | %s → %s | %s → %s | %s → %s | %s → %s |'%(k,f(x['piso_ruido_dBFS']),f(y['piso_ruido_dBFS']),origem(x['origem_ruido']),
      f(x['LUFS_voz']),f(y['LUFS_voz']),f(x['LUFS_fora_da_voz']),f(y['LUFS_fora_da_voz']),f(x['ST_med']),f(y['ST_med']),f(x['TP_dBTP']),f(y['TP_dBTP']),
      f(x['HF_4k_rel_dB']),f(y['HF_4k_rel_dB']),f(mono('../a/rev5.wav',t0,t1)),f(mono('../a/v6.wav',t0,t1))))
print('\nReel inteiro: **%s → %s LUFS integrados**, pico verdadeiro no WAV %s → %s dBTP. Clipping: %d → %d amostras. DC: 0 → 0.'%(f(a['REEL INTEIRO']['LUFS_I']),f(b['REEL INTEIRO']['LUFS_I']),f(a['REEL INTEIRO']['TP_dBTP']),f(b['REEL INTEIRO']['TP_dBTP']),a['REEL INTEIRO']['clip_amostras'],b['REEL INTEIRO']['clip_amostras']))
