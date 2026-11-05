"""Alinhamento forçado palavra a palavra (torchaudio MMS_FA) sobre o texto de cada fala.
Saída: build/palavras.json com início e fim de cada palavra no tempo da voz montada."""
import json, re, unicodedata, torch, torchaudio, soundfile as sf
L = json.load(open("build/linha_voz.json"))
NUM = {"19":"dezenove","18":"dezoito","6":"seis","3":"tres","2002":"dois mil e dois","GTA":"ge te a","Wynwood":"uainwud","Sahara":"sarara","Heat":"rit",
       "Kaseya":"caseia","Rockstar":"roquistar","Ocean":"ouchan","Drive":"draive","Colony":"coloni","Y":"ipsilon","Vice":"vaice","City":"siti","Miami":"maiami","videogame":"videogueime"}
def norm(w):
    w = NUM.get(w, w)
    w = unicodedata.normalize("NFKD", w).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z' ]", "", w).replace("'", "")
bundle = torchaudio.pipelines.MMS_FA
model = bundle.get_model(); tok = bundle.get_tokenizer(); aligner = bundle.get_aligner()
x, sr = sf.read("build/voz_crua.wav", dtype="float32")
out = []
for f in L["falas"]:
    a, b = f["inicio"], f["fim"]
    seg = torch.tensor(x[int(a*sr):int(b*sr)]).unsqueeze(0)
    seg = torchaudio.functional.resample(seg, sr, bundle.sample_rate)
    shown = f["texto"].replace("-", " ").split()   # palavras como aparecem na legenda
    spoken = [norm(re.sub(r"[^\w']", "", w)) for w in shown]
    pieces = [s.split() for s in spoken]
    flat = [p for ps in pieces for p in ps]
    with torch.inference_mode():
        em, _ = model(seg)
        spans = aligner(em[0], tok(flat))
    ratio = seg.shape[1] / em.shape[1] / bundle.sample_rate
    k = 0
    for w, ps in zip(shown, pieces):
        s0 = spans[k][0].start * ratio; s1 = spans[k+len(ps)-1][-1].end * ratio; k += len(ps)
        out.append({"fala": f["id"], "palavra": w, "inicio": round(a+s0, 3), "fim": round(a+s1, 3)})
json.dump(out, open("build/palavras.json","w"), ensure_ascii=False, indent=1)
print(" ".join(f"{o['palavra']}[{o['inicio']:.2f}]" for o in out))
