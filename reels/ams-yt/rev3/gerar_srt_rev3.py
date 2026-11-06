"""Legenda fechada (.srt) da REV3 (DS V2, 3.4.1): Português (Brasil), UTF-8, até 2 linhas de 42 caracteres,
833 ms a 7 s por legenda, quebra por sentido, no relógio do vídeo final (com gancho e decupagem).

Muda da REV1 (`rev1/gerar_srt_rev1.py`):
  - gancho e fechamento saem do que o Diego gravou (transcrição das narrações), não do roteiro;
  - as falas reais do gancho saem da transcrição da fonte, no trecho do take;
  - quem fala (`_tmp/falantes.json`, `scripts/quem_fala.py`, pelo tom de voz): quando a outra pessoa fala 3 palavras
    ou mais seguidas, abre legenda nova. Nome ("Marina: …") não entra: o DS só pede quando a pessoa não aparece, e
    isso a medição de voz não sabe dizer;
  - só sai do .srt a palavra que caiu num corte manual; palavra que o Whisper pôs numa pausa tirada é erro de tempo.

Base: transcrição automática (faster-whisper large-v3) — NÃO é verdade: o Diego ouve e confirma antes do envio
(ele vai mandar as correções do .srt depois, 23/10/2026).

Roda de reels/ams-yt:  python rev3/gerar_srt_rev3.py
Saídas: rev3/legenda_rev3.srt e rev3/legenda_duvidas_rev3.md
"""
import json
import re
import sys

sys.path.insert(0, "rev3")
import montar_rev3 as mt  # noqa: E402

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
    (r"\barroba primeirodiaem\b", "@primeirodiaem"),
    (r"(\w) -(\w)", r"\1-\2"),  # o Whisper separa palavra com hífen em dois tokens ("guarda -chuva")
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
FRACAS = {"a", "o", "de", "da", "do", "e", "que", "em", "no", "na", "um", "uma", "pra", "com", "se"}


def corrige(texto):
    for a, b in NOMES:
        texto = re.sub(a, b, texto)
    return texto


def quebra(txt):
    """Duas linhas por sentido: corta no espaço mais perto do meio que não deixe artigo/preposição no fim da 1ª linha."""
    if len(txt) <= MAX_LINHA:
        return txt
    fracas = FRACAS | {"as", "os", "das", "dos", "nos", "nas", "pro", "por", "não", "é", "eu", "a gente"}
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
    lt = json.load(open("rev3/linha_do_tempo_rev3.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    fal = json.load(open("_tmp/falantes.json", encoding="utf-8"))
    tn = json.load(open("_tmp/narr/transcricao_narr.json", encoding="utf-8"))
    mp = mt.Mapa(edl, lt["gancho_ms"])
    quem_palavra = {round(w["ini"], 3): w.get("quem", "?") for f in fal["frases"] for w in f["palavras"]}
    # a decupagem só tira pausa onde a energia da voz cai: palavra que o Whisper pôs dentro de uma pausa tirada é erro
    # de tempo da transcrição e fica (ex.: o "vale" de "vale muito a pena", 29:58). Só sai o que caiu num corte manual.
    manuais = [(r["de_s"], r["de_s"] + r["dur_s"]) for r in edl["removidos"] if r["motivo"] != "pausa na fala"]

    def mantida(t):
        return 0 <= t < edl["duracao_fonte_s"] and not any(a <= t < b for a, b in manuais)

    # frases do corpo no relógio final; palavras em trechos cortados saem; a troca de quem fala parte a frase
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
            ws.append({"p": w["p"], "ini": ini, "fim": max(fim, ini + 80), "prob": w["prob"], "quem": quem_palavra.get(round(w["ini"], 3), "?")})
        if not ws:
            continue
        baixas_todas += [w for w in ws if w["prob"] < 0.45 and len(w["p"]) > 3]
        # troca de quem fala só conta quando a outra pessoa fala 3 palavras ou mais seguidas: trecho menor vira de quem
        # fala mais na frase (uma palavra isolada do outro lado é quase sempre erro de oitava do pYIN: "Gente, meu / cabelo")
        corridas = []
        for w in ws:
            if w["quem"] in ("D", "M"):
                if corridas and corridas[-1][0] == w["quem"]:
                    corridas[-1][1].append(w)
                else:
                    corridas.append((w["quem"], [w]))
        if len(corridas) > 1:
            conta = {q: sum(len(g) for q2, g in corridas if q2 == q) for q, _ in corridas}
            maioria = max(conta, key=conta.get)
            for q, grupo in corridas:
                if len(grupo) < 3:
                    for w in grupo:
                        w["quem"] = maioria
        atual, dono = [ws[0]], ws[0]["quem"]
        for w in ws[1:]:
            if w["quem"] in ("D", "M") and dono in ("D", "M") and w["quem"] != dono:
                frases.append(atual)
                atual = []
            if w["quem"] in ("D", "M"):
                dono = w["quem"]
            atual.append(w)
        frases.append(atual)

    # gancho: falas reais dos takes com som "fala" (transcrição da fonte no trecho do take)
    pos = 0
    for c, p in zip(mt.GANCHO, [x for x in lt["audio"] if x["tipo"].startswith("gancho")]):
        if c["som"] == "fala":
            ws = []
            for s_ in tr["segmentos"]:
                for w in s_["palavras"]:
                    if c["de"] <= (w["ini"] + w["fim"]) / 2 < c["ate"]:
                        ini = p["out"] + max(0.0, w["ini"] - c["de"]) * 1000
                        ws.append({"p": w["p"], "ini": ini, "fim": min(p["out"] + p["dur"], ini + (w["fim"] - w["ini"]) * 1000), "prob": w["prob"]})
            if ws:
                frases.append(ws)
    # narrações do gancho e do fechamento (como o Diego falou)
    narr_baixas = []
    for n in lt["narracoes"]:
        chave = n["arq"].replace("/", "_").replace(".m4a", "")
        ws = []
        for w in tn[chave]["palavras"]:
            i0 = max(w["ini"], n["arq_ini_s"])
            ini = n["fala_ini"] + (i0 - n["arq_ini_s"]) * 1000
            fim = n["fala_ini"] + (max(w["fim"], i0 + 0.08) - n["arq_ini_s"]) * 1000
            ws.append({"p": w["p"], "ini": ini, "fim": min(fim, n["fala_fim"] + 150), "prob": w["prob"]})
        narr_baixas += [w for w in ws if w["prob"] < 0.6]
        frases.append(ws)
    frases.sort(key=lambda f: f[0]["ini"])

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
            if ws[i - 1]["p"].endswith((",", ".", "?", "!", ":")):
                n += 6
            if ws[i]["ini"] - ws[i - 1]["fim"] > 300:
                n += 4
            if ws[i - 1]["p"].lower().strip(",") in FRACAS:
                n -= 8
            if n > nota:
                melhor, nota = i, n
        if melhor is None:
            return [ws]
        return pedacos(ws[:melhor]) + pedacos(ws[melhor:])

    def dono(pc):
        q = [w.get("quem", "?") for w in pc if w.get("quem") in ("D", "M")]
        return max(set(q), key=q.count) if q else "?"

    blocos = [pc for f in frases for pc in pedacos(f)]
    # junta pedaços curtos com o seguinte (cada um numa linha) quando cabem, estão perto e são da mesma pessoa
    cues = []
    for pc in blocos:
        t = corrige(" ".join(w["p"] for w in pc))
        if cues:
            ant = cues[-1]
            ta = corrige(" ".join(w["p"] for w in ant["ws"]))
            mesma = dono(ant["ws"]) == dono(pc) or "?" in (dono(ant["ws"]), dono(pc))
            if mesma and "\n" not in ant["txt"] and len(ta) <= MAX_LINHA and len(t) <= MAX_LINHA and pc[0]["ini"] - ant["ws"][-1]["fim"] < 350 and pc[-1]["fim"] - ant["ws"][0]["ini"] <= MAX_DUR:
                ant["ws"] += pc
                ant["txt"] = ta + "\n" + t
                continue
        cues.append({"ws": list(pc), "txt": t})

    final = [[c["ws"][0]["ini"], c["ws"][-1]["fim"] + 250, c["txt"]] for c in cues if c["txt"].strip()]
    final.sort()

    # durações: mínimo 833 ms, máximo 7 s, sem sobrepor a próxima; respeita os 20 s da tela final (sem fala)
    for i, it in enumerate(final):
        prox = final[i + 1][0] if i + 1 < len(final) else lt["duracao_ms"] - 20000
        if it[1] - it[0] < MIN_DUR:
            it[1] = it[0] + MIN_DUR
        ideal = len(it[2].split()) / 3 * 1000  # 3 palavras/s
        if it[1] - it[0] < ideal:
            it[1] = it[0] + ideal
        it[1] = min(it[1], it[0] + MAX_DUR, prox - 40)
    rapidas = sum(1 for it in final if len(it[2].split()) / max(0.001, (it[1] - it[0]) / 1000) > 3.0)

    for it in final:
        linhas_ = it[2].split("\n")
        if any(len(x) > MAX_LINHA for x in linhas_):
            it[2] = quebra(" ".join(linhas_))
    longas = sum(1 for it in final for x in it[2].split("\n") if len(x) > MAX_LINHA)
    with open("rev3/legenda_rev3.srt", "w", encoding="utf-8") as f:
        for k, (ini, fim, txt) in enumerate(final, 1):
            f.write(f"{k}\n{ts(ini)} --> {ts(fim)}\n{txt if chr(10) in txt else quebra(txt)}\n\n")

    # lista de escuta: dúvidas conhecidas + palavras com probabilidade baixa
    linhas = ["# REV3 · Legenda: o que o Diego precisa ouvir antes de subir o .srt", "",
              "A legenda é transcrição automática (Whisper large-v3) com os nomes corrigidos para a grafia oficial. Ninguém ouviu. Antes do envio, confira estes pontos (tempo no **vídeo final** da REV3).", "",
              "## Gancho e fechamento", "", "Saem da transcrição das suas narrações (gancho gravado em 22/10, fechamento em 23/10/2026): o que você falou, não o roteiro. Palavras com confiança abaixo de 0,6:", ""]
    linhas += [f"- {ts(w['ini'])[:8]} · {corrige(w['p'])} ({w['prob']:.2f})" for w in narr_baixas] or ["- nenhuma"]
    linhas += ["", "## Trechos com dúvida", "", "| Vídeo final | Texto na legenda | Dúvida |", "|---|---|---|"]
    for chave, nota in DUVIDAS:
        for ini, fim, txt in final:
            if chave.lower() in txt.lower():
                linhas.append(f"| {ts(ini)[:8]} | {txt.replace(chr(10), ' / ')} | {nota} |")
                break
    linhas += ["", f"## Palavras com confiança baixa ({len(baixas_todas)})", "", "| Vídeo final | Palavra | Confiança |", "|---|---|---:|"]
    for w in baixas_todas:
        linhas.append(f"| {ts(w['ini'])[:8]} | {corrige(w['p'])} | {w['prob']:.2f} |")
    open("rev3/legenda_duvidas_rev3.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print(f"legendas {len(final)} · acima de 3 palavras/s: {rapidas} · linhas acima de {MAX_LINHA}: {longas} · palavras com confiança baixa: {len(baixas_todas)} (+{len(narr_baixas)} nas narrações)")


if __name__ == "__main__":
    main()
