"""Montagem da REV5 (FINAL) do vlog de Bruges (vídeo longo do YouTube, 16:9, 24 fps): gancho + corpo decupado +
fechamento + tela final, com todos os objetos e efeitos, no relógio do vídeo final.

Roda de reels/bruges-yt:  python -I rev5/montar_rev5.py
Escreve: rev5/props_rev5.json (Remotion `VideoLongo`), rev5/linha_do_tempo_rev5.json (trechos de áudio, narrações gravadas,
janelas de música), rev5/efeitos_rev5.md, rev5/takes_rev5.md, rev5/musica_janelas_rev5.json.

O corpo é o da REV4 aprovada (mesma decupagem: rev5/edl_rev5.json = rev4/edl_rev4.json, mesmos objetos, legendas e
música). Mudam (pedido do Diego, 21/11/2026): o gancho e o fechamento, reencaixados nas narrações GRAVADAS
(rev5/encaixe_rev5.py), e o fim do hotel no vídeo (sem a frase, sem a linha no Recibo, sem hotel nas contas).
Sem nenhum texto de guia (prévia): é o render final.
"""
import bisect
import importlib.util
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def _carrega(nome, pasta=AQUI):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(pasta, f"{nome}.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = _carrega("roteiro_rev5")
P = _carrega("encaixe_rev5")
FPS = R.FPS
TELA_FINAL = 20000
eur, brl = P.eur, P.brl

INI_CORPO = R.CHEGADA[0]  # 10,10 s da fonte: "Acabamos de chegar aqui em Bruges"
FIM_CORPO = R.FIM_CORPO   # 882,55 s: "…não tem um defeito, venham demais."
TIMELAPSE = (736.71, 752.79, 4.0)  # Marina soprando o waffle quente, 4× (pedido do Diego, 12:16); 1 quadro para dentro de cada corte

# Faixas (Biblioteca de áudio do YouTube; fonte/musica/): as da REV3/REV4 aprovadas (rev3/MUSICA_REV3.md)
FAIXA = {
    "G": "Bright Skies - Audio Hertz",
    "M1": "Top Of The Morning - TrackTribe",
    "M2": "Ripples In Time - Asher Fulero",
    "M3": "Swing Haven 1 - Los Angeles - Reed Mathis",
    "M4": "Starlight on the Water - Chris Haugen",
    "M5": "Peaked My Interest - Nathan Moore",
    "F": "Spring Migration - The Great North Sound Society",
}
INICIO = {"G": 12.0, "M1": 1.0, "M2": 3.0, "M3": 0.0, "M4": 0.0, "M5": 9.0, "F": 15.0}

MUSICA = [
    ("M1", "Chegada e o primeiro waffle", "leve, curiosa, manhã", [(51.66, 72.16), (100.28, 118.76)]),
    ("M2", "Markt, Burg e canais: o conto de fadas", "encantadora e empolgante", [(147.53, 160.69), (214.11, 233.22), (271.96, 302.39), (343.55, 366.49)]),
    ("M3", "Fome, chocolate e a batata", "animada e gostosa", [(458.35, 475.12), (497.94, 516.22), (604.97, 621.99)]),
    ("M4", "Minnewater: o descanso", "calma", [(676.44, 696.71)]),
    ("M5", "O teste dos waffles e a despedida", "brincalhona", [(696.71, 710.06), (TIMELAPSE[0], TIMELAPSE[1]), (816.55, 827.95)]),
]

LEGENDAS = [
    {"de": 72.40, "ate": 99.10, "por": "Diego: \"coloque legenda de 1:12 até 1:40\" (Chez Albert)"},
    {"de": 477.60, "ate": 496.95, "por": "Diego: \"Fala do 7:55 até o final de minha fala, com legenda também\" (Fritbar)"},
    {"texto_fixo": [("O", 761.38, 761.52), ("outro,", 761.55, 761.94), ("por", 763.46, 763.90), ("muito!", 764.00, 764.56)],
     "por": "Diego: \"12:40 – legende essa parte, eu falo 'o outro por muito'\". O Whisper ouve \"muito, muito, muito\": tempo das palavras estimado"},
]

ETIQUETAS = [  # (fonte s, lugar, detalhe). Hora = hora do arquivo no acervo (acervo/bruges/indice.tsv)
    (148.00, "Markt", "praça do mercado · 11H47"),
    (234.30, "Burg", "prefeitura e Basílica · 12H00"),
    (302.80, "Rozenhoedkaai", "canais · 12H46"),
    (422.60, "Igreja de Nossa Senhora", "torre de tijolos · 13H12"),
    (498.20, "Fritbar", "batata belga · 13H57"),
    (676.80, "Minnewater", "Lago do Amor · 14H47"),
]
DUR_ETIQUETA = 4000

INSTAGRAM = [217.30, 459.00]
LIKE = 285.00

FOTO_RELIQUIA = {"de": 389.00, "ate": 398.00, "arquivo": "basilica_reliquia_frasco.jpg", "x": 1250, "y": 110, "largura": 600, "altura": 398,
                 "foco": "50% 62%", "rotulo": "RELÍQUIA DO", "destino": "SANGUE SAGRADO", "credito": "foto: Matt Hopkins · CC BY-SA 2.0 · Wikimedia Commons"}
NOTA_HORARIO = {"de": 381.40, "dur": 4.6}
BILHETE_WAFFLE = {"de": 696.80, "ate": 702.50}


def q(t):
    return round(t * FPS)


def ms(s):
    return round(s * 1000)


class Mapa:
    """Fonte (s) → vídeo final (ms) no corpo, pelos trechos mantidos da decupagem e o time-lapse."""

    def __init__(self, trechos):
        self.tr = trechos
        self.ini_src = [t["src"] for t in trechos]

    def ms(self, t):
        x = t * 1000
        i = bisect.bisect_right(self.ini_src, x) - 1
        i = max(0, min(i, len(self.tr) - 1))
        tr = self.tr[i]
        v = tr.get("vel", 1)
        fim_src = tr["src"] + (tr["ate"] - tr["de"]) * v
        if x > fim_src:
            if i + 1 < len(self.tr):
                return self.tr[i + 1]["de"]
            return tr["ate"]
        return tr["de"] + (x - tr["src"]) / v


def trechos_corpo(G):
    edl = json.load(open("rev5/edl_rev5.json", encoding="utf-8"))
    assert edl["fps"] == FPS
    a0, a1 = q(INI_CORPO), q(FIM_CORPO)
    t0, t1, vel = q(TIMELAPSE[0]), q(TIMELAPSE[1]), TIMELAPSE[2]
    pedacos = []
    for qa, qb in edl["manter"]:
        qa, qb = max(qa, a0), min(qb, a1)
        if qb <= qa:
            continue
        for x, y, v in [(qa, min(qb, t0), 1), (max(qa, t0), min(qb, t1), vel), (max(qa, t1), qb, 1)]:
            if y > x:
                pedacos.append((x, y, v))
    out, pos = [], G
    for x, y, v in pedacos:
        dur = (y - x) * 1000 / FPS / v
        out.append({"src": x * 1000 / FPS, "de": pos, "ate": pos + dur, "vel": v})
        pos += dur
    return out, pos, edl


def palavras():
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    return sorted([w for s in tr["segmentos"] for w in s["palavras"] if w["fim"] > w["ini"]], key=lambda w: w["ini"])


def grupos_legenda(ws, mp, cortes_src):
    """Grupos de até 6 palavras (≤ 42 caracteres, 1 linha), quebrando em pontuação e em corte da decupagem."""
    grupos = []
    for L in LEGENDAS:
        if "texto_fixo" in L:
            pal = [{"p": p, "ini": a, "fim": b} for p, a, b in L["texto_fixo"]]
        else:
            pal = [{"p": w["p"], "ini": w["ini"], "fim": w["fim"]} for w in ws if w["ini"] >= L["de"] - 0.05 and w["fim"] <= L["ate"] + 0.3]
        g = []
        for w in pal:
            texto = " ".join(x["p"] for x in g + [w])
            quebra = g and (len(texto) > 42 or len(g) >= 6 or any(g[-1]["fim"] <= c <= w["ini"] + 0.01 for c in cortes_src) and w["ini"] - g[-1]["fim"] > 0.6)
            if quebra:
                grupos.append(g)
                g = []
            g.append(w)
            if w["p"][-1:] in ".?!" and len(g) >= 2:
                grupos.append(g)
                g = []
        if g:
            grupos.append(g)
    out = []
    for g in grupos:
        pw = [{"p": w["p"], "ini": round(mp.ms(w["ini"])), "fim": round(mp.ms(w["fim"]))} for w in g]
        ini, fim = pw[0]["ini"], max(pw[-1]["fim"] + 250, pw[0]["ini"] + 833)
        out.append({"ini": ini, "fim": fim, "palavras": pw})
    for a, b in zip(out, out[1:]):
        if a["fim"] > b["ini"] - 40:
            a["fim"] = b["ini"] - 40
    return out


def narracoes_ms(N, base_ms):
    """Narrações no relógio final (ms), com o que a mixagem precisa: arquivo, onde cai o t = 0 dele e onde a fala começa/acaba."""
    out = []
    for n in N.values():
        f = P.FALA[n["arq"]]
        out.append({"id": n["id"], "arq": n["arq"], "t0_ms": base_ms + n["T0"] * 1000, "fala_ini": base_ms + ms(n["ini"]), "fala_fim": base_ms + ms(n["fim"]),
                    "arq_ini_s": f["fala_ini_s"], "arq_fim_s": f["fala_fim_s"], "texto": n["texto"]})
    return out


def main():
    efeitos = []

    def ef(t, nome, porque, dur=None):
        efeitos.append({"ms": t, "nome": nome, "porque": porque, "dur": dur})

    # ---------------- gancho ----------------
    ev, gtk, Ng, G_s = P.props_gancho()
    G = ms(G_s)
    gancho_tr = [{"src": ms(t["src"]), "de": ms(t["de"]), "ate": ms(t["ate"]), "som": t["som"], "o_que": t["o_que"]} for t in gtk]
    narr = narracoes_ms(Ng, 0)

    # ---------------- corpo ----------------
    corpo, B_fim, edl = trechos_corpo(G)
    mp = Mapa(corpo)
    ws = palavras()

    ef(G + 500, "Placa \"1 DIA EM BRUGES →\" (Chegada + clack)", "Marca do vídeo (doc. do vídeo longo, seção 2) sobre a chegada na estação de Bruges", 3700)
    ef(G + 1000, "Data \"16 DE MARÇO DE 2026\" no painel do Placar", "Como em Bruxelas (pedido do Diego de 06/11/2026)", 3600)
    t_rec_trem = [e for e in ev if e["tipo"] == "recibo"][0]["ini"]
    ef(t_rec_trem, "Recibo do trem: € 72,00 (€ 18 por trecho, por pessoa) + Placar 09:44", "Pedido do Diego (\"18 euros por trecho por pessoa\"); entra no corte para o bilhete, no \"E a conta começa aqui\" da G5 gravada", G - t_rec_trem)

    t_m0, t_m1 = mp.ms(32.20), mp.ms(38.40)
    ev.append({"tipo": "mapa", "arquivo": "mapa_trem.json", "ini": t_m0, "fim": t_m1, "desenho": 2600})
    ef(t_m0, "Mapa Bruxelas → Bruges (Rota amarela, Pin 1º em Bruges; whoosh + plim)", "Pedido do Diego (\"coloca um mapinha\") na fala do trem", t_m1 - t_m0)

    soma = sum(v for _, v in R.GASTOS[0]["linhas"])
    for g in R.GASTOS[1:]:
        t = mp.ms(g["t"])
        total = sum(v for _, v in g["linhas"])
        antes = soma
        soma += total
        ev.append({"tipo": "placar", "ligar": t - 200, "desligar": t + 3400,
                   "valores": [{"em": t - 200, "tempo": g["hora"], "gasto": eur(antes)}, {"em": t + 400, "tempo": g["hora"], "gasto": eur(soma)}]})
        ev.append({"tipo": "recibo", "lugar": g["lugar"], "cabecalho": f"SEG 16/03 · {g['hora'].replace(':', 'H')} · BRUGES",
                   "linhas": [[n, eur(v)] for n, v in g["linhas"]], "total": eur(total), "real": "≈ " + brl(total * R.COTACAO),
                   "rodape": R.RODAPE, "ini": t, "fim": t + 5500, "x": 1400, "y": 150, "escala": 0.72})
        ef(t, f"Recibo {g['lugar']}: {eur(total)} + Placar {g['hora']} · {eur(soma)}", g["porque"], 5500)
    assert abs(soma - R.contas()["total"]) < 0.005

    for t_src, lugar, det in ETIQUETAS:
        t = mp.ms(t_src)
        ev.append({"tipo": "etiqueta", "lugar": lugar, "detalhe": det, "ini": t, "fim": t + DUR_ETIQUETA})
        ef(t, f"Etiqueta de lugar: {lugar} · {det}", "Lugar novo (DS 5.4 lower third). Hora do arquivo no acervo", DUR_ETIQUETA)

    f = FOTO_RELIQUIA
    t0, t1 = mp.ms(f["de"]), mp.ms(f["ate"])
    ev.append({"tipo": "foto", "arquivo": f["arquivo"], "x": f["x"], "y": f["y"], "largura": f["largura"], "altura": f["altura"], "foco": f["foco"],
               "rotulo": f["rotulo"], "destino": f["destino"], "credito": f["credito"], "ini": t0, "fim": t1})
    ef(t0, "Foto da relíquia do Sangue Sagrado no canto direito + placa \"RELÍQUIA DO SANGUE SAGRADO\"", "Pedido do Diego (imagem \"meio escanteada\"). Foto de Matt Hopkins, CC BY-SA 2.0", t1 - t0)
    t = mp.ms(NOTA_HORARIO["de"])
    ev.append({"tipo": "nota", "titulo": "horário da relíquia", "linhas": ["todo dia, das 14h às 16h", "(site oficial)"], "ini": t, "fim": t + NOTA_HORARIO["dur"] * 1000,
               "x": 1300, "y": 140, "largura": 520, "icone": "relogio"})
    ef(t, "Nota \"horário da relíquia: todo dia, das 14h às 16h (site oficial)\"", "Diego (21/11/2026): \"é 14 às 16, corrija minha frase\" (holyblood.com)", NOTA_HORARIO["dur"] * 1000)

    t0, t1 = mp.ms(BILHETE_WAFFLE["de"]), mp.ms(BILHETE_WAFFLE["ate"])
    ev.append({"tipo": "bilhete", "texto": "viemos dar uma chance|para um novo waffle...", "x": 1080, "y": 120, "escala": 0.85, "entrada": t0, "saida": t1})
    ef(t0, "Bilhete: \"viemos dar uma chance para um novo waffle...\"", "Pedido do Diego: \"11:36 – coloque escrito na tela\"", t1 - t0)

    tl0, tl1 = mp.ms(TIMELAPSE[0]), mp.ms(TIMELAPSE[1] - 0.001)
    ev.append({"tipo": "nota", "titulo": "tá quente!", "linhas": ["esperando esfriar…", "4× mais rápido"], "ini": tl0 + 150, "fim": tl1 - 150, "x": 1290, "y": 140, "largura": 500, "icone": "relogio"})
    ev.append({"tipo": "som", "nome": "whoosh", "em": tl0, "relDb": -8})
    ef(tl0, "Time-lapse 4× da Marina soprando o waffle quente + nota \"tá quente!\" + whoosh", "Pedido do Diego: \"12:16 – … time lapse com um efeito engraçado\"", tl1 - tl0)

    cortes_src = [r["de_s"] for r in edl["removidos"]]
    leg = grupos_legenda(ws, mp, cortes_src)
    ev.append({"tipo": "legenda", "grupos": leg})
    for L in LEGENDAS:
        de = L["texto_fixo"][0][1] if "texto_fixo" in L else L["de"]
        ate = L["texto_fixo"][-1][2] if "texto_fixo" in L else L["ate"]
        ef(mp.ms(de), f"Legenda embutida que acende palavra a palavra (fonte {de:.1f}–{ate:.1f} s)", L["por"], mp.ms(ate) - mp.ms(de))

    for t_src in INSTAGRAM:
        t = mp.ms(t_src)
        ev.append({"tipo": "instagram", "ini": t, "fim": t + 4000})
        ef(t, "Chamada SEGUE NO INSTAGRAM @primeirodiaem", "Doc. do vídeo longo: 3 vezes", 4000)
    t = mp.ms(LIKE)
    ev.append({"tipo": "like", "entrada": t, "saida": t + 3900})
    ef(t, "Animação \"DEIXA O LIKE E SE INSCREVE →\" (versão curta)", "Doc. do vídeo longo: 30–40% do vídeo", 3900)

    # ---------------- fechamento ----------------
    B = round(B_fim)
    evf, ftk, Nf, F_s = P.props_fechamento(B)
    ev += evf
    narr += narracoes_ms(Nf, B)
    fech_tr = [{"src": ms(t["src"]), "de": B + ms(t["de"]), "ate": B + ms(t["ate"]), "o_que": t["o_que"]} for t in ftk]
    fech_tr[0]["de"] = B_fim  # emenda exata com o corpo
    # a página vira sobre o ÚLTIMO QUADRO congelado (como na REV4)
    ult = fech_tr[-1]
    q1 = 1000 / FPS
    fech_tr.append({"src": round(ult["src"] + (ult["ate"] - ult["de"]) - q1), "de": ult["ate"], "ate": ult["ate"] + q1, "congela": True, "pagina": True})
    F_fim = ult["ate"] + q1
    ev.append({"tipo": "telafinal", "ini": F_fim, "proximo": R.PROXIMO})
    for e in evf:
        if e["tipo"] == "recibo":
            ef(e["ini"], "Recibo \"1 DIA EM BRUGES\": comida e bebida € 60,00 + trem € 72,00 = € 132,00 (€ 66,00/pessoa ≈ R$ 399,14)",
               "F4 gravada: \"tudo que nós consumimos aqui, mais o transporte saindo de Bruxelas, ficou 132 euros para o casal\". REV5: sem a linha do hotel (Diego, 21/11/2026)", e["fim"] - e["ini"])
        elif e["tipo"] in ("bilhete", "like", "placa"):
            ef(e["entrada"], {"bilhete": "Bilhete \"vale muito! voltaria mil vezes\"", "like": "Like e inscrição (fechamento)", "placa": "Placa final \"TODA CIDADE TEM UM PRIMEIRO DIA.\""}[e["tipo"]], "Fechamento, na palavra da narração gravada", e["saida"] - e["entrada"])
        elif e["tipo"] in ("nota", "instagram"):
            ef(e["ini"], "Nota \"dica: durma 1 noite em Bruges\"" if e["tipo"] == "nota" else "Instagram (3ª chamada)", "Fechamento, na palavra da narração gravada", e["fim"] - e["ini"])
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: paris →\")", "Ordem dos vlogs (CLAUDE.md, pendência 11)", TELA_FINAL)
    duracao = round(F_fim + TELA_FINAL)

    # ---------------- trechos e áudio ----------------
    trechos, audio = [], []
    for t in gancho_tr:
        trechos.append({"src": t["src"], "de": t["de"], "ate": t["ate"]})
        if t["som"] == "fala":
            audio.append({"src": t["src"], "out": t["de"], "dur": t["ate"] - t["de"], "tipo": "gancho_fala"})
    corpo_img = []
    for t in corpo:
        tr = {"src": round(t["src"]), "de": t["de"], "ate": t["ate"]}
        if t["vel"] != 1:
            tr["velocidade"] = t["vel"]
        corpo_img.append(tr)
        if t["vel"] == 1:
            audio.append({"src": t["src"], "out": t["de"], "dur": t["ate"] - t["de"], "tipo": "corpo"})
    for cg in edl.get("congelar", []):
        a0, a1 = mp.ms(cg["de"]), mp.ms(cg["ate"])
        novos = []
        for tr_ in corpo_img:
            if tr_["de"] < a1 and tr_["ate"] > a0 and "congela" not in tr_ and "velocidade" not in tr_:
                if tr_["de"] < a0:
                    novos.append({**tr_, "ate": a0})
                novos.append({"src": round(cg["quadro"] * 1000), "de": max(a0, tr_["de"]), "ate": min(a1, tr_["ate"]), "congela": True})
                if tr_["ate"] > a1:
                    novos.append({**tr_, "src": tr_["src"] + round(a1 - tr_["de"]), "de": a1})
            else:
                novos.append(tr_)
        corpo_img = novos
        ef(a0, f"Quadro congelado ({(a1 - a0) / 1000:.2f} s)", cg["motivo"], a1 - a0)
    trechos += corpo_img
    for t in fech_tr:
        tr = {"src": t["src"], "de": t["de"], "ate": t["ate"]}
        for k in ("pagina", "congela"):
            if t.get(k):
                tr[k] = True
        trechos.append(tr)
    for x, y in zip(trechos, trechos[1:]):
        assert abs(x["ate"] - y["de"]) < 1, (x, y)

    janelas = []
    for mid, nome, clima, js in MUSICA:
        for s0, s1 in js:
            janelas.append({"id": mid, "nome": nome, "clima": clima, "ini": round(mp.ms(s0)), "fim": round(mp.ms(s1 - 0.001)), "fonte": [s0, s1]})
    janelas.append({"id": "G", "nome": "Abertura (gancho)", "clima": "empolgante, termina na compra do bilhete", "ini": 0, "fim": G, "fonte": None})
    janelas.append({"id": "F", "nome": "Fechamento e tela final", "clima": "alegre e calorosa", "ini": round(B_fim), "fim": duracao, "fonte": None})

    props = {"video": P.VIDEO, "duracao": duracao, "fps": FPS, "trechos": trechos, "eventos": ev, "zooms": [], "refLufs": -16, "semGrao": True}
    json.dump(props, open("rev5/props_rev5.json", "w", encoding="utf-8"), ensure_ascii=False)
    ng = [n for n in narr if n["id"].startswith("G")]
    nf = [n for n in narr if n["id"].startswith("F")]
    json.dump({"fps": FPS, "gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio,
               "narracoes": narr, "musica": janelas, "faixas": FAIXA, "inicio_faixa_s": INICIO,
               "narracao_fim_gancho_ms": max(n["fala_fim"] for n in ng), "fechamento_narr_fim_ms": max(n["fala_fim"] for n in nf),
               "contas": R.contas(), "keen_ms": None},
              open("rev5/linha_do_tempo_rev5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(t):
        s = t / 1000
        return f"{int(s // 60)}:{s % 60:04.1f}".replace(".", ",")

    efeitos.sort(key=lambda e: e["ms"])
    with open("rev5/efeitos_rev5.md", "w", encoding="utf-8") as fh:
        fh.write("# REV5 · Efeitos e objetos (vlog de Bruges, final)\n\nTempos no vídeo final da REV5 (" + mmss(duracao) + "). Gerado por `rev5/montar_rev5.py`.\n\n")
        fh.write("| Entra | Dura | Efeito | Por quê |\n|---|---:|---|---|\n")
        for e in efeitos:
            dur = "" if e["dur"] is None else f"{e['dur'] / 1000:.1f} s".replace(".", ",")
            fh.write(f"| {mmss(e['ms'])} | {dur} | {e['nome']} | {e['porque']} |\n")
    with open("rev5/takes_rev5.md", "w", encoding="utf-8") as fh:
        fh.write("# REV5 · Takes e narrações do gancho e do fechamento (vlog de Bruges, final)\n\n")
        fh.write("Encaixados nas narrações gravadas (`rev5/encaixe_rev5.py`): o corte cai na palavra dita; todo take ≥ 2 s e dentro de um plano.\n\n")
        fh.write("| Bloco | No vídeo | Fonte | O que é |\n|---|---|---|---|\n")
        for t in gancho_tr:
            fh.write(f"| Gancho | {mmss(t['de'])}–{mmss(t['ate'])} ({(t['ate'] - t['de']) / 1000:.2f} s) | {t['src'] / 1000:.2f}–{(t['src'] + t['ate'] - t['de']) / 1000:.2f} | {t['o_que']} |\n")
        for t in fech_tr:
            if t.get("congela"):
                continue
            fh.write(f"| Fechamento | {mmss(t['de'])}–{mmss(t['ate'])} ({(t['ate'] - t['de']) / 1000:.2f} s) | {t['src'] / 1000:.2f}–{(t['src'] + t['ate'] - t['de']) / 1000:.2f} | {t['o_que']} |\n")
        fh.write("\n| Narração | Arquivo | No vídeo (fala) | Texto (como foi dito) |\n|---|---|---|---|\n")
        for n in narr:
            fh.write(f"| {n['id']} | {n['arq']}.m4a | {mmss(n['fala_ini'])}–{mmss(n['fala_fim'])} | {n['texto']} |\n")
    with open("rev5/musica_janelas_rev5.json", "w", encoding="utf-8") as fh:
        json.dump(janelas, fh, ensure_ascii=False, indent=1)
    print(f"gancho {mmss(G)} · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} · total {mmss(duracao)} · {len(trechos)} trechos · {len(ev)} eventos · {q(duracao / 1000)} quadros")
    print(f"  legendas: {len(leg)} grupos; contas {R.contas()}")


if __name__ == "__main__":
    main()
