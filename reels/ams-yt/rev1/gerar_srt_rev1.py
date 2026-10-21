"""Legenda fechada (.srt) da REV1 (DS V2, 3.4.1): Português (Brasil), UTF-8, até 2 linhas de 42 caracteres,
833 ms a 7 s por legenda, quebra por sentido, no relógio do vídeo final (com gancho e decupagem).

Base: transcrição automática (faster-whisper large-v3) — NÃO é verdade: o Diego ouve e confirma antes do envio.
Nomes de lugares vão na grafia oficial (conferida no OpenStreetMap e nos sites oficiais); o resto fica como foi dito.
As falas do gancho e do fechamento vêm do roteiro da narração e precisam ser refeitas depois da gravação.

Roda de reels/ams-yt:  python rev1/gerar_srt_rev1.py
Saídas: rev1/legenda_rev1.srt e rev1/legenda_duvidas_rev1.md
"""
import json
import re
import sys

sys.path.insert(0, "rev1")
import montar_rev1 as mt  # noqa: E402

MAX_LINHA = 42
MAX_DUR = 7000
MIN_DUR = 833

# grafia oficial dos nomes (o som é o mesmo; muda só como se escreve)
NOMES = [
    (r"\bAmsterdã\b", "Amsterdam"), (r"\bmuseum blind\b", "Museumplein"), (r"\bDating Houses\b", "Dancing Houses"),
    (r"\bPraça Dan\b", "Praça Dam"), (r"\bmannequin piece\b", "Manneken Pis"), (r"\bKalvenstraat\b", "Kalverstraat"),
    (r"\bTutu Waffle\b", "stroopwafels"), (r"\bestruco waffle\b", "stroopwafel"), (r"\bStroopwafel\b", "stroopwafel"),
    (r"\bThe Full Bell\b", "The Old Bell"), (r"\bLa Chouf\b", "La Chouffe"), (r"\bHeadlight District\b", "Red Light District"),
    (r"\bHeadlight\b", "Red Light"), (r"\bAmistel\b", "Amstel"), (r"\bHeim\b", "Heineken"), (r"\bN\. Frank\b", "Anne Frank"),
    (r"\bM-Train\b", "Anne Frank"), (r"\bAlbert Cooke Market\b", "Albert Cuyp Market"), (r"\bAlbert Cuit Market\b", "Albert Cuyp Market"),
    (r"\bLouris\b", "Rudi's"), (r"\bStu Coffin\b", "stroopwafel"), (r"\bMouco\b", "Moco"), (r"\bfable fries\b", "Fabel Friet"),
    (r"\bbairro de ordem\b", "bairro Jordaan"), (r"\bMac Crisp\b", "McCrispy"), (r"\bno Mac\b", "no McDonald's"),
    (r"\bSarfat Park\b", "Sarphatipark"), (r"\bThe Pipe\b", "De Pijp"), (r"\bDejip, Deuip\b", "De Pijp"),
    (r"\bChegamos na Fable\b", "Chegamos na FEBO"), (r"\bMarie Heineken Klein\b", "Marie Heinekenplein"),
    (r"\bbelgica bruxelas\b", "Bélgica, Bruxelas"), (r"\bfebo\b", "FEBO"), (r"\bVangog\b", "Van Gogh"),
    (r"\bA comida típica é uma roupa frita\b", "A comida típica é uma batata frita"),
]
# trechos que a transcrição não resolve: vão para a lista de escuta do Diego (não são inventados no .srt)
DUVIDAS = [
    ("sol macio", "02:25 da fonte: \"Por causa do sol macio\" — palavra provável errada"),
    ("Amistadão", "07:06 da fonte: \"Obrigado, Amistadão\" (Amsterdam?)"),
    ("viado", "07:14 da fonte: \"Pra basicamente só atravessar um viado\" — provavelmente outra palavra"),
    ("Fih", "12:48 da fonte: \"o Fih não tinha jantado\" (apelido?)"),
    ("guinfonado", "28:39 da fonte: \"que é o guinfonado com molhinho e alface\" (frango empanado?)"),
    ("Kiko", "08:29 da fonte: \"Pull&Bear agora, Kiko\" (loja KIKO Milano?)"),
    ("Saparte", "25:02 da fonte: \"acho que é Saparte, parque não\" (Sarphatipark)"),
    ("Riges", "19:35 da fonte: \"Riges... alguma coisa\" — mantido como foi dito (Rijksmuseum)"),
    ("primeira fábrica", "28:57 da fonte: \"Ele chegou no ... A primeira fábrica\" — a transcrição sem filtro ouviu \"parque de rações\""),
]


def corrige(texto):
    for a, b in NOMES:
        texto = re.sub(a, b, texto)
    return texto


def quebra(txt):
    """Duas linhas por sentido: corta no espaço mais perto do meio que não deixe artigo/preposição no fim da 1ª linha."""
    if len(txt) <= MAX_LINHA:
        return txt
    fracas = {"a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "e", "que", "pra", "pro", "com", "por", "se", "não", "é", "eu", "a gente"}
    espacos = [i for i, c in enumerate(txt) if c == " "]
    melhor = None
    for i in sorted(espacos, key=lambda i: abs(i - len(txt) / 2)):
        l1, l2 = txt[:i], txt[i + 1:]
        if len(l1) <= MAX_LINHA and len(l2) <= MAX_LINHA and l1.split()[-1].lower() not in fracas:
            melhor = i
            break
    if melhor is None:
        validos = [i for i in espacos if i <= MAX_LINHA and len(txt) - i - 1 <= MAX_LINHA]
        melhor = min(validos or espacos, key=lambda i: abs(i - len(txt) / 2))
    return txt[:melhor] + "\n" + txt[melhor + 1:]


def ts(ms):
    ms = max(0, int(round(ms)))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))
    lt = json.load(open("rev1/linha_do_tempo_rev1.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    mp = mt.Mapa(edl, lt["gancho_ms"])
    manter = [(a / 24, b / 24) for a, b in edl["manter"]]

    def mantida(t):
        return any(a <= t < b for a, b in manter)

    # frases (segmentos da transcrição) do corpo no relógio final; palavras em trechos cortados saem
    frases = []
    baixas_todas = []
    ultima = None
    for s_ in tr["segmentos"]:
        ws = []
        for w in s_["palavras"]:
            # palavra repetida na emenda de dois trechos da transcrição (duração ~0, confiança < 0,1): sai
            if ultima and w["prob"] < 0.1 and w["p"].strip(".,!?").lower() == ultima["p"].strip(".,!?").lower() and w["ini"] - ultima["fim"] < 0.1:
                continue
            ultima = w
            c = (w["ini"] + w["fim"]) / 2
            if not mantida(c):
                continue
            ini, fim = mp.ms(w["ini"]), mp.ms(min(w["fim"], w["ini"] + 1.2))
            ws.append({"p": w["p"], "ini": ini, "fim": max(fim, ini + 80), "prob": w["prob"]})
        if ws:
            frases.append(ws)
            baixas_todas += [w for w in ws if w["prob"] < 0.45 and len(w["p"]) > 3]
    palavras = [w for f in frases for w in f]

    def pedacos(ws):
        """Divide uma frase em pedaços de até 80 caracteres: corta em vírgula, pausa > 300 ms ou, sem opção, no meio."""
        txt = " ".join(w["p"] for w in ws)
        if len(corrige(txt)) <= 74 and ws[-1]["fim"] - ws[0]["ini"] <= MAX_DUR:
            return [ws]
        melhor, nota = None, -1e9
        for i in range(1, len(ws)):
            l1 = len(corrige(" ".join(w["p"] for w in ws[:i])))
            l2 = len(corrige(" ".join(w["p"] for w in ws[i:])))
            if l1 < 12 or l2 < 12:
                continue
            n = -abs(l1 - l2) / 10
            if ws[i - 1]["p"].endswith((",", ".", "?", "!")):
                n += 6
            if ws[i]["ini"] - ws[i - 1]["fim"] > 300:
                n += 4
            if ws[i - 1]["p"].lower().strip(",") in {"a", "o", "de", "da", "do", "e", "que", "em", "no", "na", "um", "uma", "pra", "com", "se"}:
                n -= 8
            if n > nota:
                melhor, nota = i, n
        if melhor is None:
            return [ws]
        return pedacos(ws[:melhor]) + pedacos(ws[melhor:])

    blocos = [pc for f in frases for pc in pedacos(f)]
    # junta pedaços curtos com o seguinte (cada um numa linha) quando cabem e estão perto
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

    itens = []
    # gancho e fechamento: roteiro da narração (a confirmar depois da gravação) + falas reais do gancho
    reais = {211.9: "Gente, meu cabelo!", 1159.6: "Surreal.", 1865.3: "Bebi quatro, estou realizado."}
    for p in lt["audio"]:
        if p["tipo"] == "gancho_fala":
            itens.append([p["out"] + 150, p["out"] + p["dur"] - 100, reais.get(round(p["src"], 1), "")])
    for ini, fim, txt in lt["narracao_gancho"]:
        itens.append([ini, fim, txt])
    for c in cues:
        itens.append([c["ws"][0]["ini"], c["ws"][-1]["fim"] + 250, c["txt"]])
    for ini, fim, txt in lt["narracao_fechamento"]:
        itens.append([ini, fim, txt])
    itens = [i for i in itens if i[2].strip()]
    itens.sort()

    # divide frases de narração longas em pedaços de até 2 linhas, proporcionalmente ao tamanho
    final = []
    for ini, fim, txt in itens:
        if "\n" in txt or len(txt) <= 80:
            final.append([ini, fim, txt])
            continue
        partes, atual = [], ""
        for pal in txt.split():
            if len(atual) + len(pal) + 1 > 76 and atual:
                partes.append(atual)
                atual = pal
            else:
                atual = f"{atual} {pal}".strip()
        partes.append(atual)
        tot = sum(len(x) for x in partes)
        t = ini
        for x in partes:
            d = (fim - ini) * len(x) / tot
            final.append([t, t + d, x])
            t += d

    # durações: mínimo 833 ms, máximo 7 s, sem sobrepor a próxima; respeita os 20 s da tela final (sem fala)
    for i, it in enumerate(final):
        prox = final[i + 1][0] if i + 1 < len(final) else lt["duracao_ms"] - 20000
        if it[1] - it[0] < MIN_DUR:
            it[1] = it[0] + MIN_DUR
        palavras_n = len(it[2].split())
        ideal = palavras_n / 3 * 1000  # 3 palavras/s
        if it[1] - it[0] < ideal:
            it[1] = it[0] + ideal
        it[1] = min(it[1], it[0] + MAX_DUR, prox - 40)
    rapidas = sum(1 for it in final if len(it[2].split()) / max(0.001, (it[1] - it[0]) / 1000) > 3.0)

    for it in final:
        linhas_ = it[2].split("\n")
        if any(len(x) > MAX_LINHA for x in linhas_):
            it[2] = quebra(" ".join(linhas_))
    longas = sum(1 for it in final for x in it[2].split("\n") if len(x) > MAX_LINHA)
    print(f"linhas acima de {MAX_LINHA} caracteres: {longas}")
    with open("rev1/legenda_rev1.srt", "w", encoding="utf-8") as f:
        for k, (ini, fim, txt) in enumerate(final, 1):
            f.write(f"{k}\n{ts(ini)} --> {ts(fim)}\n{txt if chr(10) in txt else quebra(txt)}\n\n")

    # lista de escuta: dúvidas conhecidas + palavras com probabilidade baixa
    linhas = ["# REV1 · Legenda: o que o Diego precisa ouvir antes de subir o .srt", "",
              "A legenda é transcrição automática (Whisper large-v3) com os nomes corrigidos para a grafia oficial. Ninguém ouviu. Antes do envio, confira estes pontos (tempo no **vídeo final**).", "",
              "## Trechos com dúvida", "", "| Vídeo final | Texto na legenda | Dúvida |", "|---|---|---|"]
    for chave, nota in DUVIDAS:
        for ini, fim, txt in final:
            if chave.lower() in txt.lower():
                linhas.append(f"| {ts(ini)[:8]} | {txt} | {nota} |")
                break
    baixas = baixas_todas
    linhas += ["", f"## Palavras com confiança baixa ({len(baixas)})", "", "| Vídeo final | Palavra | Confiança |", "|---|---|---:|"]
    for w in baixas:
        linhas.append(f"| {ts(w['ini'])[:8]} | {corrige(w['p'])} | {w['prob']:.2f} |")
    linhas += ["", "## Gancho e fechamento", "", "As legendas do gancho e do fechamento são o **roteiro** da narração. Depois da gravação, eu ajusto o texto e o tempo ao que você disse.", ""]
    open("rev1/legenda_duvidas_rev1.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print(f"legendas {len(final)} · acima de 3 palavras/s: {rapidas} · palavras com confiança baixa: {len(baixas)}")


if __name__ == "__main__":
    main()
