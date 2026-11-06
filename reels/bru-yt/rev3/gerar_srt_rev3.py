"""Legenda fechada (.srt) da REV3 do vlog de Bruxelas (DS V2, 3.4.1; doc. do vídeo longo, seção 2): Português (Brasil),
UTF-8, até 2 linhas de 42 caracteres, 833 ms a 7 s por legenda, quebra por sentido, no relógio do vídeo final (gancho,
corpo decupado, hotel e fechamento). Método do vlog de Amsterdam (`reels/ams-yt/rev3/gerar_srt_rev3.py`), sem a
separação por falante (não foi medida neste vídeo): a frase parte em pausa de mais de 600 ms ou em pontuação.

Base: transcrição automática (faster-whisper large-v3) da fonte e das narrações — NÃO é verdade: o Diego ouve e
confirma antes do envio (`legenda_duvidas_rev3.md`). Nomes na grafia oficial; o resto como foi transcrito.

Roda de reels/bru-yt:  python rev3/gerar_srt_rev3.py   →  rev3/legenda_rev3.srt e rev3/legenda_duvidas_rev3.md
"""
import json
import re
from bisect import bisect_right

MAX_LINHA = 42
MAX_DUR = 7000
MIN_DUR = 833
FPS = 30

NOMES = [
    (r"\bAtômico\b", "Atomium"), (r"\bAtômio\b", "Atomium"), (r"\bAtomium,", "Atomium,"),
    (r"\bGran Plácido\b", "Grand Place"), (r"\bgrand place\b", "Grand Place"), (r"\bbruxelas\b", "Bruxelas"),
    (r"\bR \$3 ,50\b", "3,50 euros"), (r"\bR \$5\b", "5 euros"),  # o Whisper escreveu reais; o Diego falou euros (valores do registro)
    (r"\bLe Madalena\b", "Le Madeleine"), (r"\bSpago\b", "Spago"), (r"\bFritland\b", "Fritland"),
    (r"\barroba primeirodiaem\b", "@primeirodiaem"), (r"\b1738\b", "1.738"),
    (r"\bBate e Volta\b", "bate e volta"), (r"\bpro Bruxelas\b", "por Bruxelas"), (r"\baforrar\b", "forrar"),
    (r"\bSaint -François\b", "Saint-François"), (r"(\w) -(\w)", r"\1-\2"),
]
# trechos que a transcrição não resolve: vão para a lista de escuta (não são inventados no .srt)
DUVIDAS = [
    ("Phil", "2:32 da fonte: \"É do Phil?\" — palavra provável errada"),
    ("alaifante", "3:04 da fonte: \"isso daqui não é um alaifante\" (elefante?)"),
    ("pata", "3:17 da fonte: \"A pata xangou?\" — palavra provável errada"),
    ("Praça Dourada", "4:03 da fonte: \"Estamos aqui na Praça Dourada\" — conferir"),
    ("Praia 360", "4:05 da fonte: \"Praia 360.\" (Praça 360?)"),
    ("Saint-François", "6:30 da fonte: \"Galeria Royale de Saint-François\" — o nome é Saint-Hubert; ficou como foi dito"),
    ("Madeleine", "10:51 da fonte: \"chamado Le Madalena\": escrito Le Madeleine (Brasserie de la Madeleine)"),
    ("Marcos", "12:26 da fonte: \"o frio desumano que o Marcos tá sentindo\" (a Marina?)"),
    ("por Bruxelas", "F1 (narração): o Whisper ouviu \"pro Bruxelas\"; escrito \"por Bruxelas\""),
]
FRACAS = {"a", "o", "de", "da", "do", "e", "que", "em", "no", "na", "um", "uma", "pra", "com", "se", "as", "os", "das", "dos", "nos", "nas", "pro", "por", "não", "é", "eu"}


def corrige(t):
    for a, b in NOMES:
        t = re.sub(a, b, t)
    return t


def quebra(txt):
    if len(txt) <= MAX_LINHA:
        return txt
    esp = [i for i, c in enumerate(txt) if c == " "]
    for i in sorted(esp, key=lambda i: abs(i - len(txt) / 2)):
        l1, l2 = txt[:i], txt[i + 1:]
        if len(l1) <= MAX_LINHA and len(l2) <= MAX_LINHA and l1.split()[-1].lower() not in FRACAS:
            return l1 + "\n" + l2
    validos = [i for i in esp if i <= MAX_LINHA and len(txt) - i - 1 <= MAX_LINHA]
    i = min(validos or esp, key=lambda i: abs(i - len(txt) / 2))
    return txt[:i] + "\n" + txt[i + 1:]


def ts(ms):
    ms = max(0, int(round(ms)))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    lt = json.load(open("rev3/linha_do_tempo_rev3.json", encoding="utf-8"))
    edl = json.load(open("rev3/edl_rev3.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    tn = json.load(open("_tmp/narr/transcricao_narracoes.json", encoding="utf-8"))
    G, corpo_fim = lt["gancho_ms"], lt["corpo_fim_ms"]
    manter = lt["manter"]
    ini_src = [a / FPS for a, _ in manter]
    acc, ini_out = 0, []
    for a, b in manter:
        ini_out.append(acc)
        acc += b - a

    def ms(t):
        i = bisect_right(ini_src, t) - 1
        if i < 0:
            return None
        a, b = manter[i]
        if t * FPS >= b:
            return None
        return G + (ini_out[i] + t * FPS - a) * 1000 / FPS

    manuais = [(r["de_s"], r["de_s"] + r["dur_s"]) for r in edl["removidos"] if not r["motivo"].startswith("pausa")]
    frases, baixas = [], []
    # corpo
    for s_ in tr["segmentos"]:
        ws = []
        for w in s_["palavras"]:
            c = (w["ini"] + w["fim"]) / 2
            if any(a <= c < b for a, b in manuais) or c >= 862.2:
                continue
            i0 = ms(w["ini"]) or ms(w["ini"] + 0.05)
            if i0 is None:
                continue
            i1 = ms(min(w["fim"], w["ini"] + 1.2)) or i0 + 300
            ws.append({"p": w["p"], "ini": i0, "fim": max(i1, i0 + 80), "prob": w["prob"]})
        if ws:
            baixas += [w for w in ws if w["prob"] < 0.45 and len(w["p"]) > 3]
            frases.append(ws)
    # falas reais do gancho (transcrição da fonte no trecho do som de cada take): entra a palavra que COMEÇA dentro
    # do take (o fim do Whisper estica sobre a pausa: "mijando.", "vitrine."); pedaços seguidos viram uma frase só
    ws = []
    fim_ant = None
    for p in lt["audio"]:
        if p["tipo"] != "gancho_fala":
            continue
        if fim_ant is not None and p["out"] - fim_ant > 50 and ws:
            frases.append(ws)
            ws = []
        for s_ in tr["segmentos"]:
            for w in s_["palavras"]:
                if p["src"] - 0.02 <= w["ini"] < p["src"] + p["dur"] / 1000 - 0.08:
                    ini = p["out"] + (w["ini"] - p["src"]) * 1000
                    ws.append({"p": w["p"], "ini": max(p["out"], ini), "fim": min(p["out"] + p["dur"], ini + (w["fim"] - w["ini"]) * 1000), "prob": w["prob"]})
        fim_ant = p["out"] + p["dur"]
    if ws:
        frases.append(ws)
    # narrações (como o Diego falou), com os cortes internos (F1)
    narr_baixas = []
    for n in lt["narracoes"]:
        chave = n["arq"].split("/")[-1].replace(".m4a", "")
        cortes = n.get("cortes", [])
        ws = []
        for w in tn[chave]:
            c = (w["ini"] + w["fim"]) / 2
            if any(a <= c < b for a, b in cortes):
                continue
            desc = sum(b - a for a, b in cortes if b <= w["ini"])
            i0 = max(w["ini"], n["arq_ini_s"])
            ini = n["fala_ini"] + (i0 - n["arq_ini_s"] - desc) * 1000
            fim = n["fala_ini"] + (max(w["fim"], i0 + 0.08) - n["arq_ini_s"] - desc) * 1000
            ws.append({"p": w["p"], "ini": ini, "fim": min(fim, n["fala_fim"] + 150), "prob": w["prob"]})
        narr_baixas += [w for w in ws if w["prob"] < 0.6]
        frases.append(ws)
    frases.sort(key=lambda f: f[0]["ini"])

    def pedacos(ws):
        txt = corrige(" ".join(w["p"] for w in ws))
        if len(txt) <= 74 and ws[-1]["fim"] - ws[0]["ini"] <= MAX_DUR:
            return [ws]
        melhor, nota = None, -1e9
        for i in range(1, len(ws)):
            l1 = len(corrige(" ".join(w["p"] for w in ws[:i])))
            l2 = len(corrige(" ".join(w["p"] for w in ws[i:])))
            if l1 < 12 or l2 < 12:
                continue
            sc = -abs(l1 - l2) / 10
            if ws[i - 1]["p"].endswith((",", ".", "?", "!", ":")):
                sc += 6
            if ws[i]["ini"] - ws[i - 1]["fim"] > 300:
                sc += 4
            if ws[i - 1]["p"].lower().strip(",") in FRACAS:
                sc -= 8
            if sc > nota:
                melhor, nota = i, sc
        if melhor is None:
            return [ws]
        return pedacos(ws[:melhor]) + pedacos(ws[melhor:])

    # parte as frases também em pausas longas (> 600 ms): sem medição de falante, é onde a vez costuma trocar
    partes = []
    for f in frases:
        atual = [f[0]]
        for w in f[1:]:
            if w["ini"] - atual[-1]["fim"] > 600:
                partes.append(atual)
                atual = []
            atual.append(w)
        partes.append(atual)
    blocos = [pc for f in partes for pc in pedacos(f)]
    cues = []
    for pc in blocos:
        t = corrige(" ".join(w["p"] for w in pc))
        if cues:
            ant = cues[-1]
            ta = corrige(" ".join(w["p"] for w in ant["ws"]))
            if "\n" not in ant["txt"] and len(ta) <= MAX_LINHA and len(t) <= MAX_LINHA and pc[0]["ini"] - ant["ws"][-1]["fim"] < 350 and pc[-1]["fim"] - ant["ws"][0]["ini"] <= MAX_DUR:
                ant["ws"] += pc
                ant["txt"] = ta + "\n" + t
                continue
        cues.append({"ws": list(pc), "txt": t})
    final = sorted([[c["ws"][0]["ini"], c["ws"][-1]["fim"] + 250, c["txt"]] for c in cues if c["txt"].strip()])
    for i, it in enumerate(final):
        prox = final[i + 1][0] if i + 1 < len(final) else lt["duracao_ms"] - 20000
        if it[1] - it[0] < MIN_DUR:
            it[1] = it[0] + MIN_DUR
        ideal = len(it[2].split()) / 3 * 1000
        if it[1] - it[0] < ideal:
            it[1] = it[0] + ideal
        it[1] = min(it[1], it[0] + MAX_DUR, prox - 40)
        if any(len(x) > MAX_LINHA for x in it[2].split("\n")):
            it[2] = quebra(" ".join(it[2].split("\n")))
    longas = sum(1 for it in final for x in it[2].split("\n") if len(x) > MAX_LINHA)
    with open("rev3/legenda_rev3.srt", "w", encoding="utf-8") as fo:
        for k, (ini, fim, txt) in enumerate(final, 1):
            fo.write(f"{k}\n{ts(ini)} --> {ts(fim)}\n{txt}\n\n")

    L = ["# REV3 · Legenda: o que ouvir antes de subir o .srt (vlog de Bruxelas)", "",
         "A legenda é transcrição automática (Whisper large-v3) com os nomes na grafia oficial. Ninguém ouviu. Tempos no **vídeo final** da REV3.", "",
         "## Narrações (gancho, hotel e fechamento): palavras com confiança abaixo de 0,6", ""]
    L += [f"- {ts(w['ini'])[:8]} · {corrige(w['p'])} ({w['prob']:.2f})" for w in narr_baixas] or ["- nenhuma"]
    L += ["", "## Trechos com dúvida", "", "| Vídeo final | Texto na legenda | Dúvida |", "|---|---|---|"]
    for chave, nota in DUVIDAS:
        for ini, fim, txt in final:
            if chave.lower() in txt.lower().replace("\n", " "):
                L.append(f"| {ts(ini)[:8]} | {txt.replace(chr(10), ' / ')} | {nota} |")
                break
    L += ["", f"## Palavras com confiança baixa ({len(baixas)})", "", "| Vídeo final | Palavra | Confiança |", "|---|---|---:|"]
    L += [f"| {ts(w['ini'])[:8]} | {corrige(w['p'])} | {w['prob']:.2f} |" for w in baixas]
    open("rev3/legenda_duvidas_rev3.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"legendas {len(final)} · linhas acima de {MAX_LINHA}: {longas} · confiança baixa: {len(baixas)} (+{len(narr_baixas)} nas narrações)")


if __name__ == "__main__":
    main()
