"""Alinhamento forçado palavra a palavra (torchaudio MMS_FA) sobre o texto do Whisper large-v3.
Roda de reels/culinaria-europa:  python3 rev1/scripts/alinhar.py _tmp/voz16k.wav _tmp/transcricao.json rev1/transcricao_alinhada.json
A transcrição é automática; a validação auditiva é humana."""
import json, re, sys, unicodedata
import soundfile as sf, torch, torchaudio

NUM = {"7": "sete", "3": "tres", "20": "vinte", "4": "quatro"}
def norm(w):
    w = NUM.get(re.sub(r"[^\w]", "", w), w)
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z]", "", w)

wav, sr = sf.read(sys.argv[1], dtype="float32"); assert sr == 16000
segs = json.load(open(sys.argv[2]))
bundle = torchaudio.pipelines.MMS_FA
model = bundle.get_model(with_star=False).eval()
dic = bundle.get_dict(star=None)
out = []
for s in segs:
    a = max(0.0, s["ini"] - 0.25); b = min(len(wav) / sr, s["fim"] + 0.25)
    chunk = torch.from_numpy(wav[int(a * sr):int(b * sr)]).unsqueeze(0)
    pal = [w for w in s["palavras"]]
    toks = [norm(w["p"]) for w in pal]
    with torch.inference_mode():
        em, _ = model(chunk)
    tgt = torch.tensor([[dic[c] for t in toks for c in t]], dtype=torch.int32)
    ali, sc = torchaudio.functional.forced_align(em, tgt, blank=0)
    spans = torchaudio.functional.merge_tokens(ali[0], sc[0].exp())
    ratio = chunk.shape[1] / em.shape[1] / sr
    i = 0
    for w, t in zip(pal, toks):
        sp = spans[i:i + len(t)]; i += len(t)
        ini = a + sp[0].start * ratio; fim = a + sp[-1].end * ratio
        conf = sum(x.score for x in sp) / len(sp)
        out.append({"p": w["p"], "ini": round(ini, 3), "fim": round(fim, 3), "whisper_ini": w["ini"], "conf": round(float(conf), 3)})
json.dump({"fonte": "fala_diego.mp4", "metodo": "faster-whisper large-v3 + torchaudio MMS_FA", "palavras": out}, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
for w in out:
    flag = " <<" if w["conf"] < 0.5 or abs(w["ini"] - w["whisper_ini"]) > 0.3 else ""
    print(f'{w["ini"]:6.2f} {w["fim"]:6.2f} {w["conf"]:.2f} {w["p"]}{flag}')
