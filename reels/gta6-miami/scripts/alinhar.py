"""Alinhamento forçado palavra a palavra (wav2vec2 PT, CTC) de cada tomada de edicao.json.
Saída: transcricao_alinhada.json com início e fim de cada palavra no tempo da gravação original.
Uso (de dentro de reels/gta6-miami): python3 scripts/alinhar.py"""
import json, subprocess
import numpy as np, torch, torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

ed = json.load(open("edicao.json"))
MOD = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
proc = Wav2Vec2Processor.from_pretrained(MOD)
model = Wav2Vec2ForCTC.from_pretrained(MOD).eval()
voc = proc.tokenizer.get_vocab()
SR = 16000
audio = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", ed["fonte"], "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                                     capture_output=True, check=True).stdout, np.float32)
saida = []
for tom in ed["tomadas"]:
    t0, t1 = tom["janela"]
    seg = audio[int(t0 * SR):int(t1 * SR)]
    inp = proc(seg, sampling_rate=SR, return_tensors="pt", padding=True)
    with torch.inference_mode():
        lp = torch.log_softmax(model(inp.input_values).logits, dim=-1)
    palavras = tom["texto"].split()
    alvo = "|".join(palavras)
    ids = [voc[c] for c in alvo]
    ali, sc = torchaudio.functional.forced_align(lp, torch.tensor([ids]), blank=voc["<pad>"])
    ali, sc = ali[0].tolist(), sc[0].exp().tolist()
    passo = seg.shape[0] / SR / lp.shape[1]
    # spans de cada caractere do alvo (sequência CTC: repetições e brancos)
    spans, k, prev = [], -1, None
    for f, (tok, s) in enumerate(zip(ali, sc)):
        if tok == voc["<pad>"]:
            prev = None
            continue
        if tok != prev:
            k += 1
            spans.append([f, f, [s]])
        else:
            spans[-1][1] = f
            spans[-1][2].append(s)
        prev = tok
    assert k + 1 == len(ids), (tom["id"], k + 1, len(ids))
    i = 0
    for w in palavras:
        cs = spans[i:i + len(w)]
        saida.append({"tomada": tom["id"], "falado": w, "ini": round(t0 + cs[0][0] * passo, 3), "fim": round(t0 + (cs[-1][1] + 1) * passo, 3),
                      "conf": round(float(np.mean([x for c in cs for x in c[2]])), 3)})
        i += len(w) + 1
    print(tom["id"], " ".join(f"{p['falado']}[{p['ini']:.2f}-{p['fim']:.2f}]" for p in saida if p["tomada"] == tom["id"]), flush=True)
json.dump(saida, open("transcricao_alinhada.json", "w"), ensure_ascii=False, indent=1)
