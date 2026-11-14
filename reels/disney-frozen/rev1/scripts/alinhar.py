"""Alinhamento forçado palavra a palavra (torchaudio MMS_FA) sobre o texto conferido de cada fala (mesmo método da Disney Parte 2).
O texto vem do Whisper large-v3 corrigido onde ele errou ("parque e roupa" → "park hopper"). 'in'/'out' aqui são só a janela
de busca de cada fala (a tomada inteira); o corte final é feito em preparar.py pela energia da voz.
Lê ../edicao.json e grava ../transcricao_alinhada.json. Roda de dentro de reels/disney-frozen/rev1: python3 scripts/alinhar.py"""
import json, os, subprocess, unicodedata, re
import numpy as np, torch, torchaudio

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ed = json.load(open(os.path.join(AQUI, "edicao.json"), encoding="utf-8"))
FONTE = os.path.normpath(os.path.join(AQUI, ed["fonte_dir"]))
FALADO = {"park": "parque", "hopper": "roper"}  # pronúncia aportuguesada, como ele fala
bundle = torchaudio.pipelines.MMS_FA
modelo = bundle.get_model(with_star=False)
alinhar = bundle.get_aligner()
tok = bundle.get_tokenizer()

def roman(w):
    w = unicodedata.normalize("NFKD", w.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z']", "", w)

arq = os.path.join(FONTE, ed["fonte"])
r = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True)
a = np.frombuffer(r.stdout, dtype=np.float32)
saida = {}
for f in ed["falas"]:
    i0, i1 = int(f["in"] * 16000), int(min(f["out"], len(a) / 16000) * 16000)
    wav = torch.from_numpy(a[i0:i1].copy()).unsqueeze(0)
    palavras = f["texto"].split()
    faladas, dono = [], []
    for k, w in enumerate(palavras):
        chave = re.sub(r"[,.!?:;]$", "", w).lower()
        for p in FALADO.get(chave, w).split():
            rp = roman(p)
            if rp:
                faladas.append(rp)
                dono.append(k)
    with torch.inference_mode():
        em, _ = modelo(wav)
        spans = alinhar(em[0], tok(faladas))
    razao = wav.shape[1] / em.shape[1] / 16000
    lista = []
    for k, w in enumerate(palavras):
        sp = [s for d, s in zip(dono, spans) if d == k]
        ini = f["in"] + sp[0][0].start * razao
        fim = f["in"] + sp[-1][-1].end * razao
        sc = float(np.mean([x.score for s in sp for x in s]))
        lista.append({"texto": w, "ini": round(ini, 3), "fim": round(fim, 3), "prob": round(sc, 3)})
    saida[f["id"]] = lista
    print(f["id"], " ".join(f"{x['texto']}[{x['ini']:.2f}-{x['fim']:.2f}|{x['prob']:.2f}]" for x in lista))
json.dump(saida, open(os.path.join(AQUI, "transcricao_alinhada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
