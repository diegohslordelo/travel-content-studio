"""Alinhamento forçado (wav2vec2 PT, CTC) usado por scripts/cortes.py (no arquivo bruto) e scripts/alinhar.py (na voz decupada).
Cada palavra da legenda pode ter uma pronúncia diferente da grafia (números, siglas, nomes): PRONUNCIA dá a leitura
usada só no alinhamento; a legenda mostra a grafia. '_' numa palavra = espaço inseparável (R$_2.400)."""
import re, unicodedata
import numpy as np
import torch, torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

MODELO = "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese"
# leitura falada de cada palavra escrita (minúsculas, sem pontuação); lista = variantes, decididas pela verossimilhança
PRONUNCIA = {
    "r$_2.400": ["dois mil e quatrocentos reais"], "3": ["três"], "6,46": ["seis e quarenta e seis", "seis vírgula quarenta e seis", "seis quarenta e seis"],
    "iof": ["iofe", "i ó éfe", "i o éfe"], "hotéis.com": ["hotéis ponto com"], "r$_1.095": ["mil e noventa e cinco reais"],
    "r$_210": ["duzentos e dez reais"], "210": ["duzentos e dez"], "r$_2.385": ["dois mil trezentos e oitenta e cinco reais", "dois mil e trezentos e oitenta e cinco reais"], "840": ["oitocentos e quarenta"], "280": ["duzentos e oitenta"], "250": ["duzentos e cinquenta"],
    "2.385": ["dois mil trezentos e oitenta e cinco", "dois mil e trezentos e oitenta e cinco"], "uber": ["úber"], "bernabéu": ["bernabéu"],
    "mayor": ["maior"], "plaza": ["plaça", "plaza"],
}

_proc = _mod = None


def modelo():
    global _proc, _mod
    if _proc is None:
        _proc = Wav2Vec2Processor.from_pretrained(MODELO)
        _mod = Wav2Vec2ForCTC.from_pretrained(MODELO).eval()
    return _proc, _mod


def emissoes(x16k):
    proc, mod = modelo()
    with torch.inference_mode():
        return torch.log_softmax(mod(proc(x16k, sampling_rate=16000, return_tensors="pt").input_values).logits, dim=-1)


def chave(w):
    return w.lower().strip(".,:;!?")


def leitura(w, escolha=None):
    """Leitura de uma palavra escrita: a variante escolhida (índice) ou a 1ª de PRONUNCIA; senão a própria grafia."""
    v = PRONUNCIA.get(chave(w))
    if not v:
        return chave(w).replace("_", " ")
    return v[escolha or 0]


def ids(texto_leitura):
    proc, _ = modelo()
    voc = proc.tokenizer.get_vocab()
    out = []
    for ch in re.sub(r"[^a-záàâãéêíóôõúüç]", "", texto_leitura.lower()):
        if ch in voc:
            out.append(voc[ch])
        else:
            base = unicodedata.normalize("NFD", ch)[0]
            if base in voc:
                out.append(voc[base])
    return out


def alvo(palavras, escolhas=None):
    """Sequência de tokens (com '|' entre as palavras faladas) e o dono (índice da palavra escrita) de cada token."""
    proc, _ = modelo()
    voc = proc.tokenizer.get_vocab()
    sep = voc.get("|")
    seq, dono = [], []
    for i, w in enumerate(palavras):
        for k, parte in enumerate(leitura(w, (escolhas or {}).get(i)).split()):
            if seq and sep is not None:
                seq.append(sep); dono.append(None)
            for t in ids(parte):
                seq.append(t); dono.append(i)
    return seq, dono


def nll(em, seq):
    """−log p(texto | áudio), somando todos os alinhamentos possíveis (perda CTC)."""
    proc, _ = modelo()
    blank = proc.tokenizer.get_vocab()[proc.tokenizer.pad_token]
    lp = em.transpose(0, 1)  # (T, 1, V)
    return float(torch.nn.functional.ctc_loss(lp, torch.tensor([seq]), torch.tensor([lp.shape[0]]), torch.tensor([len(seq)]),
                                              blank=blank, reduction="sum", zero_infinity=True))


def alinhar(em, seq, dono, n, t0, passo):
    """Início, fim e probabilidade média de cada palavra escrita (segundos = t0 + quadro × passo)."""
    proc, _ = modelo()
    blank = proc.tokenizer.get_vocab()[proc.tokenizer.pad_token]
    rot, sc = torchaudio.functional.forced_align(em, torch.tensor([seq], dtype=torch.int32), blank=blank)
    rot, sc = rot[0].tolist(), sc[0].exp().tolist()
    k, prev = -1, blank
    ini, fim, prob = {}, {}, {}
    for q, (r, p) in enumerate(zip(rot, sc)):
        if r != blank and (r != prev or q == 0):
            k += 1
        if r != blank and 0 <= k < len(dono) and dono[k] is not None:
            i = dono[k]
            ini.setdefault(i, q); fim[i] = q + 1; prob.setdefault(i, []).append(p)
        prev = r
    return [(t0 + ini.get(i, 0) * passo, t0 + fim.get(i, 0) * passo, float(np.mean(prob.get(i, [0])))) for i in range(n)]
