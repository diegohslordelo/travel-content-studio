"""Decide o texto e os cortes de cada bloco de voz a partir do alinhamento forçado no arquivo BRUTO (não decupado).
1. Variantes {a|b} do texto gravado (onde o Whisper normaliza a fala ou os dois modelos discordam) e variantes de leitura
   (PRONUNCIA): fica a de menor −log p (perda CTC) — a que o áudio sustenta melhor.
2. Entrada = início da 1ª palavra − 0,08 s; saída = fim da última + 0,15 s (nenhuma palavra perde começo ou fim).
Uso (de dentro de reels/madrid-custo/): python3 scripts/cortes.py   → reescreve 'texto' e 'trechos' em edicao.json e
grava _tmp/cortes.json (palavras no tempo do bruto, com a probabilidade de cada uma)."""
import json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alinhamento import PRONUNCIA, alinhar, alvo, chave, emissoes, nll

ANTES, DEPOIS = 0.08, 0.15


def le16(f):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, dtype=np.float32)


def opcoes(texto):
    """'a {x|y} b' → partes [['a'], ['x','y'] , ['b']] em palavras."""
    out = []
    for m in re.finditer(r"\{([^}]*)\}|(\S+)", texto):
        if m.group(1) is not None:
            out.append(("var", [o.strip() for o in m.group(1).split("|")]))
        else:
            out.append(("fixo", m.group(2)))
    return out


def monta(partes, esc):
    ws = []
    for k, (tp, v) in enumerate(partes):
        ws += (v[esc.get(k, 0)].split() if tp == "var" else [v])
    return ws


d = json.load(open("edicao.json", encoding="utf-8"))
saida = {}
for fa in d["falas"]:
    x = le16(f"fonte/voz/{fa['fonte']}.m4a")
    dur = len(x) / 16000
    em = emissoes(x)
    passo = dur / em.shape[1]
    partes = opcoes(fa["texto_gravado"])
    esc, decisoes = {}, []
    for k, (tp, v) in enumerate(partes):  # variantes do texto, uma por vez
        if tp != "var":
            continue
        custos = [nll(em, alvo(monta(partes, {**esc, k: j}))[0]) for j in range(len(v))]
        esc[k] = int(np.argmin(custos))
        decisoes.append(f"{'/'.join(v)} → '{v[esc[k]]}' ({', '.join(f'{c:.1f}' for c in custos)})")
    ws = monta(partes, esc)
    lei = {}
    for i, w in enumerate(ws):  # variantes de leitura (números, siglas)
        vs = PRONUNCIA.get(chave(w), [])
        if len(vs) > 1:
            custos = [nll(em, alvo(ws, {**lei, i: j})[0]) for j in range(len(vs))]
            lei[i] = int(np.argmin(custos))
            decisoes.append(f"leitura de '{w}' → '{vs[lei[i]]}' ({', '.join(f'{c:.1f}' for c in custos)})")
    seq, dono = alvo(ws, lei)
    al = alinhar(em, seq, dono, len(ws), 0.0, passo)
    a = max(0.0, al[0][0] - ANTES)
    b = min(dur, al[-1][1] + DEPOIS)
    fa["texto"] = " ".join(ws)
    fa["trechos"] = [[round(a, 2), round(b, 2)]]
    fa["leituras"] = {ws[i]: PRONUNCIA[chave(ws[i])][j] for i, j in lei.items()}
    saida[fa["id"]] = {"palavras": [{"t": w, "ini": round(i0, 3), "fim": round(i1, 3), "prob": round(p, 3)} for w, (i0, i1, p) in zip(ws, al)],
                       "decisoes": decisoes, "dur": round(dur, 3)}
    fracas = [f"{w}({p:.2f})" for w, (_, _, p) in zip(ws, al) if p < 0.5]
    print(f"{fa['id']} {fa['fonte']} corte {a:.2f}–{b:.2f} de {dur:.2f} s · 1ª palavra {al[0][0]:.2f} · última termina {al[-1][1]:.2f}")
    print(f"   {fa['texto']}")
    for x_ in decisoes:
        print("   decisão:", x_)
    if fracas:
        print("   palavras com prob < 0,5:", ", ".join(fracas))
json.dump(d, open("edicao.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(saida, open("_tmp/cortes.json", "w"), ensure_ascii=False, indent=1)
