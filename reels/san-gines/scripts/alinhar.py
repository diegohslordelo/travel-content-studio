"""Alinhamento forçado palavra a palavra (wav2vec2 PT, CTC; torchaudio.functional.forced_align) do texto de cada bloco
(edicao.json, a fala gravada) sobre a voz já decupada (public/voz.wav). É o tempo da legenda que acende palavra a palavra.
Nomes em inglês são alinhados por uma grafia de pronúncia (só para o alinhamento; a legenda mostra a grafia certa).
Uso (de dentro de reels/san-gines/): python3 scripts/alinhar.py
Saída: _tmp/palavras.json  [{fala, texto, ini, fim, prob}] no tempo do Reel"""
import json, re, unicodedata
import numpy as np
import soundfile as sf
import torch, torchaudio
from scipy.signal import resample_poly
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
PRONUNCIA = {"1894": "miloitocentosenoventaequatro", "10": "dez", "6": "seis", "€6,50": "seisecinquenta", "€3,90": "trêsenoventa",
             "€10,40": "dezequarenta", "ginés": "guinés", "churrería": "churreria", "chocolatería": "chocolateria", "madrid": "madri",
             "puerta": "puerta", "del": "del"}

proc = Wav2Vec2Processor.from_pretrained(MODELO)
mod = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
voc = proc.tokenizer.get_vocab()
blank = voc[proc.tokenizer.pad_token]
sep = voc.get("|")


def tokens_da_palavra(w):
    w = PRONUNCIA.get(w.lower().strip(".,:;!?"), w.lower().strip(".,:;!?"))
    w = re.sub(r"[^a-záàâãéêíóôõúüç]", "", w)
    out = []
    for ch in w:
        if ch in voc:
            out.append(voc[ch])
        else:  # letra sem token: tira o acento
            base = unicodedata.normalize("NFD", ch)[0]
            if base in voc:
                out.append(voc[base])
    return out


d = json.load(open("edicao.json", encoding="utf-8"))
tre = json.load(open("_tmp/trechos.json"))
a, sr = sf.read("public/voz.wav")
x = resample_poly(a, 1, 3).astype(np.float32)  # 48 kHz → 16 kHz
saida = []
for fa in d["falas"]:
    ts = [t for t in tre if t["fala"] == fa["id"]]
    j0 = ts[0]["inicio"]; j1 = ts[-1]["inicio"] + ts[-1]["quadros"] / d["fps"]
    s0, s1 = int(max(0, j0 - 0.03) * 16000), int((j1 + 0.03) * 16000)
    with torch.inference_mode():
        em = torch.log_softmax(mod(proc(x[s0:s1], sampling_rate=16000, return_tensors="pt").input_values).logits, dim=-1)
    palavras = fa["texto"].split()
    alvo, dono = [], []
    for i, w in enumerate(palavras):
        tk = tokens_da_palavra(w.replace("-", ""))
        if alvo and sep is not None:
            alvo.append(sep); dono.append(None)
        for t in tk:
            alvo.append(t); dono.append(i)
    rot, sc = torchaudio.functional.forced_align(em, torch.tensor([alvo], dtype=torch.int32), blank=blank)
    rot, sc = rot[0].tolist(), sc[0].exp().tolist()
    passo = (s1 - s0) / 16000 / em.shape[1]
    # cada quadro de emissão não-branco pertence ao token em ordem; acha início/fim de cada palavra
    k, prev = -1, blank
    ini, fim, prob = {}, {}, {}
    for q, (r, p) in enumerate(zip(rot, sc)):
        if r != blank and (r != prev or q == 0):
            k += 1
        if r != blank and 0 <= k < len(dono) and dono[k] is not None:
            i = dono[k]
            ini.setdefault(i, q); fim[i] = q + 1; prob.setdefault(i, []).append(p)
        prev = r
    for i, w in enumerate(palavras):
        t0 = s0 / 16000 + ini.get(i, 0) * passo
        t1 = s0 / 16000 + fim.get(i, 0) * passo
        saida.append({"fala": fa["id"], "texto": w, "ini": round(t0, 3), "fim": round(t1, 3), "prob": round(float(np.mean(prob.get(i, [0]))), 3)})
json.dump(saida, open("_tmp/palavras.json", "w"), ensure_ascii=False, indent=0)
fracas = [p for p in saida if p["prob"] < 0.5]
print(f"{len(saida)} palavras alinhadas; {len(fracas)} com probabilidade < 0,5: " + ", ".join(f"{p['texto']}({p['prob']})" for p in fracas))
for fa in d["falas"]:
    ws = [p for p in saida if p["fala"] == fa["id"]]
    print(f"  {fa['id']}: " + " ".join(f"{w['texto']}[{w['ini']:.2f}]" for w in ws))
