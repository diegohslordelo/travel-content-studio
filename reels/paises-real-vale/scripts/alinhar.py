# Alinhamento forçado palavra a palavra (MMS_FA, torchaudio) de cada tomada de rev1/tomadas.json.
# Roda de dentro da pasta do Reel: python3 scripts/alinhar.py rev1
import json, sys, wave
import numpy as np, torch, torchaudio
rev = sys.argv[1]
cfg = json.load(open(f"{rev}/tomadas.json"))
w = wave.open("_tmp/audio16k.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
b = torchaudio.pipelines.MMS_FA
model = b.get_model(); dic = b.get_dict(star=None)
out = []
for t in cfg["tomadas"]:
    i, f = t["janela"]
    seg = torch.from_numpy(a[int(i*16000):int(f*16000)]).unsqueeze(0)
    with torch.inference_mode():
        em, _ = model(seg)
    # palavras faladas (cada exibição pode ter várias palavras faladas)
    faladas, dono = [], []
    for k, (_, fal) in enumerate(t["palavras"]):
        for p in fal.split():
            faladas.append(p); dono.append(k)
    toks = [dic[c] for p in faladas for c in p]
    al, sc = torchaudio.functional.forced_align(em, torch.tensor([toks], dtype=torch.int32), blank=0)
    spans = torchaudio.functional.merge_tokens(al[0], sc[0].exp())
    ratio = seg.shape[1] / em.shape[1] / 16000
    pos = 0; ws = []
    for p in faladas:
        sp = spans[pos:pos+len(p)]; pos += len(p)
        ws.append((i + sp[0].start*ratio, i + sp[-1].end*ratio, float(np.mean([s.score for s in sp]))))
    pal = []
    for k, (disp, _) in enumerate(t["palavras"]):
        idx = [j for j, d in enumerate(dono) if d == k]
        pal.append({"txt": disp, "s": round(ws[idx[0]][0], 3), "e": round(ws[idx[-1]][1], 3), "conf": round(min(ws[j][2] for j in idx), 2)})
    out.append({"id": t["id"], "janela": t["janela"], "palavras": pal})
    print(t["id"], " ".join(f"{p['txt']}({p['s']:.2f}-{p['e']:.2f},{p['conf']})" for p in pal), flush=True)
json.dump(out, open(f"{rev}/alinhamento.json", "w"), ensure_ascii=False, indent=1)
