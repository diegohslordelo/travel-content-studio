import sys, numpy as np, soundfile as sf
from scipy.ndimage import median_filter
x2,sr=sf.read(sys.argv[1],always_2d=True)
for ch in range(x2.shape[1]):
    x=x2[:,ch]
    e=np.abs(x[1:-1]-(x[:-2]+x[2:])/2)          # quanto a amostra foge da média das vizinhas
    loc=median_filter(e,size=481)+1e-6
    cand=np.where((e>8*loc)&(e>0.05))[0]+1
    evs=[]
    for c in cand:
        # isolado: as vizinhas a ±2..±6 amostras não têm desvio parecido
        viz=np.r_[e[max(0,c-7):c-2],e[c+1:c+6]]
        if e[c-1]>2*viz.max():
            if not evs or c-evs[-1]>480: evs.append(c)
    print('canal',ch,'picos isolados:',[(round(c/sr,4),round(float(x[c]),3),round(float(e[c-1]/loc[c-1]),0)) for c in evs])
