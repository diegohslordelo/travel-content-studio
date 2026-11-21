"""Legenda fechada (.srt) da REV5 (FINAL) do vlog de Bruges (DS V2, 3.4.1; padrão de áudio, seção 10): Português (Brasil),
UTF-8, até 2 linhas de 42 caracteres, 833 ms a 7 s por legenda, quebra por sentido, no relógio do vídeo final.

Base: transcrição automática (faster-whisper large-v3) — NÃO é verdade: ninguém ouviu. O Diego confere antes de subir
(lista em rev5/legenda_duvidas_rev5.md). Modelo: `reels/ams-yt/rev3/gerar_srt_rev3.py`, sem a separação por falante.

O que entra:
  - corpo: palavras da fonte que ficaram na decupagem (sai só a palavra que caiu num corte manual: palavra que o Whisper
    pôs numa pausa tirada é erro de tempo dele);
  - gancho: a fala real da Marina (take com som);
  - narrações gravadas: o texto do roteiro da REV5 (o que foi dito, conferido em 2 passadas do Whisper), com o tempo das
    palavras do Whisper alinhado palavra a palavra.
Uma legenda nunca junta dois falantes ou duas fontes (fala do vlog, fala da Marina no gancho, cada narração).
O que sai (DS 3.4.1, "eventos com reforço embutido retirados"): os 3 trechos com legenda gravada na imagem (pedido do
Diego) e o time-lapse (sem o som da fonte). Nada nos 20 s da tela final.

Roda de reels/bruges-yt:  python -I rev5/gerar_srt_rev5.py   →  rev5/legenda_rev5.srt, rev5/legenda_duvidas_rev5.md
"""
import difflib
import importlib.util
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("montar_rev5", os.path.join(AQUI, "montar_rev5.py"))
mt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mt)

MAX_LINHA = 42
MAX_DUR = 7000
MIN_DUR = 833
FRACAS = {"a", "o", "de", "da", "do", "e", "que", "em", "no", "na", "um", "uma", "pra", "com", "se"}
NOMES = [
    (r"\bChess Albert\b", "Chez Albert"), (r"\bFritz Bar\b", "Fritbar"), (r"\bGo Free\b", "Gofre"), (r"\bBasilica\b", "Basílica"),
    (r"\bMinewater Park\b", "Minnewater Park"), (r"\barroba primeirodiaem\b", "@primeirodiaem"),
    (r"(\w) -(\w)", r"\1-\2"),  # o Whisper separa palavra com hífen em dois tokens ("bate -volta")
]
DUVIDAS = [
    ("Brunswick", "\"antes de sair daqui de Brunswick Passei aqui no barzinho\": nome provável errado (13:29 da fonte)"),
    ("Jacquin", "\"Vai, Jacquin.\": palavra provável errada (11:54 da fonte)"),
    ("Minewater ou", "\"É Minewater ou é Minewater?\": você pergunta a pronúncia; ficou como o Whisper ouviu (10:33 da fonte)"),
    ("pagou 5 euros", "\"a gente pagou 5 euros na…\": valor falado; o Recibo mostra batata € 15,00 + bebidas € 8,00 (anotação \"9:55\"). Conferir se é \"15\" (9:21 da fonte)"),
    ("custa um dia", "G1 gravada: as 2 passadas do Whisper ouvem \"Quanto custam de em Bruges\"; na legenda ficou \"Quanto custa um dia em Bruges\" (o texto do roteiro)"),
    ("uma hora de Bruxelas", "G5 gravada: \"cerca de uma hora de Bruxelas\" (Whisper sem dica) ou \"…de Bruges\" (com dica, confiança 0,53)"),
]
TL = mt.TIMELAPSE


def corrige(t):
    for a, b in NOMES:
        t = re.sub(a, b, t)
    return t


def quebra(txt):
    if len(txt) <= MAX_LINHA:
        return txt
    fracas = FRACAS | {"as", "os", "das", "dos", "nos", "nas", "pro", "por", "não", "é", "eu"}
    espacos = [i for i, c in enumerate(txt) if c == " "]
    for i in sorted(espacos, key=lambda i: abs(i - len(txt) / 2)):
        l1, l2 = txt[:i], txt[i + 1:]
        if len(l1) <= MAX_LINHA and len(l2) <= MAX_LINHA and l1.split()[-1].lower() not in fracas:
            return l1 + "\n" + l2
    validos = [i for i in espacos if i <= MAX_LINHA and len(txt) - i - 1 <= MAX_LINHA]
    i = min(validos or espacos, key=lambda i: abs(i - len(txt) / 2))
    return txt[:i] + "\n" + txt[i + 1:]


def ts(ms):
    ms = max(0, int(round(ms)))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def chave(p):
    return re.sub(r"[^\wà-ú]", "", p.lower())


def main():
    lt = json.load(open("rev5/linha_do_tempo_rev5.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    tn = json.load(open("dados/transcricao_narracoes.json", encoding="utf-8"))
    corpo, B_fim, edl = mt.trechos_corpo(lt["gancho_ms"])
    mp = mt.Mapa(corpo)
    manuais = [(r["de_s"], r["de_s"] + r["dur_s"]) for r in edl["removidos"] if r["motivo"] != "pausa na fala"]
    fora = [(L["de"], L["ate"]) if "de" in L else (L["texto_fixo"][0][1] - 0.05, L["texto_fixo"][-1][2] + 0.05) for L in mt.LEGENDAS] + [(TL[0], TL[1])]

    def mantida(t):
        return mt.INI_CORPO <= t < mt.FIM_CORPO and not any(a <= t < b for a, b in manuais) and not any(a <= t < b for a, b in fora)

    # palavra que o Whisper pôs dentro de uma montagem sem fala (as janelas de música são silêncio digital na fonte) é erro
    # de tempo dele: sai da legenda, menos as de MOVER, que vão para onde são ditas (o "Uma" de "Uma coisa que eu não
    # mencionei" é dito depois da montagem do Rozenhoedkaai, logo antes de "coisa", 366,83 da fonte; REV4, conferência)
    MOVER = {343.37: (366.76, 366.83)}
    janelas = [(a, b) for _, _, _, js in mt.MUSICA for a, b in js]
    movidas = []
    for s_ in tr["segmentos"]:
        fica = []
        for w in s_["palavras"]:
            c = (w["ini"] + w["fim"]) / 2
            if any(a <= c < b for a, b in janelas):
                k = round(w["ini"], 2)
                if k in MOVER:
                    w["ini"], w["fim"] = MOVER[k]
                    movidas.append((w["p"], k, "→", MOVER[k][0]))
                else:
                    movidas.append((w["p"], k, "fora"))
                    continue
            fica.append(w)
        s_["palavras"] = fica
    frases, baixas = [], []
    ultima = None
    for s_ in tr["segmentos"]:
        ws = []
        for w in s_["palavras"]:
            if ultima and w["prob"] < 0.1 and chave(w["p"]) == chave(ultima["p"]) and w["ini"] - ultima["fim"] < 0.1:
                continue
            ultima = w
            if not mantida((w["ini"] + w["fim"]) / 2):
                continue
            ini, fim = mp.ms(w["ini"]), mp.ms(min(w["fim"], w["ini"] + 1.2))
            ws.append({"p": w["p"], "ini": ini, "fim": max(fim, ini + 80), "prob": w["prob"], "quem": "corpo"})
        if ws:
            baixas += [w for w in ws if w["prob"] < 0.45 and len(w["p"]) > 3]
            atual = [ws[0]]  # pausa de mais de 1,2 s (no relógio final) abre outra frase: legenda não entra antes da fala
            for w in ws[1:]:
                if w["ini"] - atual[-1]["fim"] > 1200:
                    frases.append(atual)
                    atual = []
                atual.append(w)
            frases.append(atual)
    # gancho: a fala real da Marina
    for p in [x for x in lt["audio"] if x["tipo"] == "gancho_fala"]:
        a, b = p["src"] / 1000, (p["src"] + p["dur"]) / 1000
        ws = [{"p": w["p"], "ini": p["out"] + max(0.0, w["ini"] - a) * 1000, "fim": min(p["out"] + p["dur"], p["out"] + (w["fim"] - a) * 1000), "prob": w["prob"], "quem": "marina"}
              for s_ in tr["segmentos"] for w in s_["palavras"] if a <= (w["ini"] + w["fim"]) / 2 < b]
        if ws:  # começo de frase e o ponto que o Whisper não pôs ("…eu já comi. E foi só uma batata frita, tá?")
            ws[0]["p"] = ws[0]["p"][:1].upper() + ws[0]["p"][1:]
            for a_, b_ in zip(ws, ws[1:]):
                if b_["p"] == "E" and not a_["p"].endswith((".", ",", "?", "!")):
                    a_["p"] += "."
            frases.append(ws)
    # narrações: texto do roteiro, tempo das palavras do Whisper (alinhadas por difflib)
    for n in lt["narracoes"]:
        W = tn[n["arq"]]["palavras"]
        C = n["texto"].split()
        sm = difflib.SequenceMatcher(a=[chave(w["p"]) for w in W], b=[chave(c) for c in C], autojunk=False)
        tempo = [None] * len(C)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op in ("equal", "replace"):
                for k in range(j2 - j1):
                    w = W[min(i1 + round(k * (i2 - i1) / max(1, j2 - j1)), max(i1, i2 - 1))]
                    tempo[j1 + k] = (max(w["ini"], n["arq_ini_s"]), w["fim"])
        for j in range(len(C)):  # palavras sem par: entre as vizinhas
            if tempo[j] is None:
                a = next((tempo[k][1] for k in range(j - 1, -1, -1) if tempo[k]), n["arq_ini_s"])
                tempo[j] = (a, a + 0.2)
        ws = [{"p": c, "ini": n["t0_ms"] + t0 * 1000, "fim": min(n["t0_ms"] + max(t1, t0 + 0.08) * 1000, n["fala_fim"] + 150), "prob": 1.0, "quem": n["id"]} for c, (t0, t1) in zip(C, tempo)]
        frases.append(ws)
    frases.sort(key=lambda f: f[0]["ini"])

    def pedacos(ws):
        txt = " ".join(w["p"] for w in ws)
        if len(corrige(txt)) <= 74 and ws[-1]["fim"] - ws[0]["ini"] <= MAX_DUR:
            return [ws]
        melhor, nota = None, -1e9
        for i in range(1, len(ws)):
            l1 = len(corrige(" ".join(w["p"] for w in ws[:i])))
            l2 = len(corrige(" ".join(w["p"] for w in ws[i:])))
            if l1 < 16 or l2 < 16:  # pedaço curto ("@primeirodiaem.") não fica sozinho
                continue
            nn = -abs(l1 - l2) / 10
            if ws[i - 1]["p"].endswith((",", ".", "?", "!", ":")):
                nn += 6
            if ws[i]["ini"] - ws[i - 1]["fim"] > 300:
                nn += 4
            if ws[i - 1]["p"].lower().strip(",") in FRACAS:
                nn -= 8
            if nn > nota:
                melhor, nota = i, nn
        if melhor is None:
            return [ws]
        return pedacos(ws[:melhor]) + pedacos(ws[melhor:])

    cues = []
    for pc in [pc for f in frases for pc in pedacos(f)]:
        t = corrige(" ".join(w["p"] for w in pc))
        if cues:
            ant = cues[-1]
            ta = corrige(" ".join(w["p"] for w in ant["ws"]))
            if ant["ws"][-1]["quem"] == pc[0]["quem"] and "\n" not in ant["txt"] and len(ta) <= MAX_LINHA and len(t) <= MAX_LINHA and pc[0]["ini"] - ant["ws"][-1]["fim"] < 350 and pc[-1]["fim"] - ant["ws"][0]["ini"] <= MAX_DUR:
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
        linhas_ = it[2].split("\n")
        if any(len(x) > MAX_LINHA for x in linhas_):
            it[2] = quebra(" ".join(linhas_))
    longas = sum(1 for it in final for x in it[2].split("\n") if len(x) > MAX_LINHA)
    tres = sum(1 for it in final if it[2].count("\n") > 1)
    assert all(it[1] <= lt["duracao_ms"] - 20000 for it in final), "legenda na tela final"
    with open("rev5/legenda_rev5.srt", "w", encoding="utf-8") as f:
        for k, (ini, fim, txt) in enumerate(final, 1):
            f.write(f"{k}\n{ts(ini)} --> {ts(fim)}\n{txt if chr(10) in txt else quebra(txt)}\n\n")
    L = ["# REV5 · Legenda (.srt): o que conferir antes de subir", "",
         "`legenda_rev5.srt` é transcrição automática (Whisper large-v3), com os nomes na grafia oficial. **Ninguém ouviu.** Confira estes pontos antes de subir (tempo no vídeo final da REV5).",
         "Ficaram fora do .srt, de propósito: os 3 trechos com legenda gravada na imagem (Chez Albert, Fritbar e \"O outro, por muito!\") e o time-lapse (sem som).", "",
         "## Trechos com dúvida", "", "| Vídeo final | Texto na legenda | Dúvida |", "|---|---|---|"]
    for ch, nota in DUVIDAS:
        achou = next((it for it in final if ch.lower() in it[2].replace("\n", " ").lower()), None)
        L.append(f"| {ts(achou[0])[:8] if achou else '—'} | {achou[2].replace(chr(10), ' / ') if achou else '(fora do .srt)'} | {nota} |")
    L += ["", f"## Palavras com confiança baixa ({len(baixas)})", "", "| Vídeo final | Palavra | Confiança |", "|---|---|---:|"]
    L += [f"| {ts(w['ini'])[:8]} | {corrige(w['p'])} | {w['prob']:.2f} |" for w in baixas]
    open("rev5/legenda_duvidas_rev5.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("palavras movidas (erro de tempo do Whisper):", movidas)
    print(f"legendas {len(final)} · linhas acima de {MAX_LINHA}: {longas} · com 3+ linhas: {tres} · palavras com confiança baixa: {len(baixas)}")


if __name__ == "__main__":
    main()
