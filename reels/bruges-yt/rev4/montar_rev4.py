"""Montagem da REV4 do vlog de Bruges (vídeo longo do YouTube, 16:9, 24 fps): gancho + corpo decupado + fechamento +
tela final, com todos os objetos e efeitos, no relógio do vídeo final.

Roda de reels/bruges-yt:  python -I rev4/montar_rev4.py [--sem-guia]
Escreve: rev4/props_rev4.json (Remotion `VideoLongo`), rev4/linha_do_tempo_rev4.json (trechos de áudio, narrações,
janelas de música), rev4/efeitos_rev4.md, rev4/takes_rev4.md, rev4/DECUPAGEM_REV4.md.

Pedidos do Diego (20/11/2026) que este script cumpre:
  - voz decupada, sem espaço entre as falas e sem os prolongamentos (scripts/decupar.py → rev4/edl_rev4.json);
  - a compra do bilhete encurtada para 4,5 s, no fim do gancho, com "18 euros por trecho por pessoa" (Recibo);
  - mapa animado Bruxelas → Bruges na fala do trem; Placar e Recibos dos gastos (foto das anotações);
  - legenda que acende palavra a palavra só em 1:12–1:40, 7:55–fim da fala e 12:40 da fonte;
  - "viemos dar uma chance para um novo waffle..." escrito na tela em 11:36 (Bilhete, letra de caneta);
  - time-lapse com efeito engraçado na Marina provando o waffle quente (12:16);
  - imagem da relíquia "meio escanteada" na fala da Basílica (Placa + recorte de foto, DS 2.6).
REV2 (Diego, 21/11/2026): sem o `keen`; mais canal no gancho; fechamento novo (frases mais fortes); waffle da 2ª ida ao
Chez Albert € 4,70; a frase "fica exposto das 12 às 16 horas" sai e o horário certo (14h–16h) entra escrito na tela;
música da Biblioteca de áudio do YouTube, uma faixa por seção (FAIXA, abaixo; mixagem em rev4/mixar_previa_rev4.py).
Na prévia, o nome da faixa aparece no topo em cada trecho de música (guia; sai no render final, --sem-guia).
"""
import argparse
import bisect
import importlib.util
import json
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def _carrega(nome):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, f"{nome}.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


R = _carrega("roteiro_rev4")
P = _carrega("previas_narracao_rev4")
FPS = R.FPS
TELA_FINAL = 20000
VALOR_CA2 = P.VALOR_CA2  # suposição só para a prévia (a confirmar)
eur, brl = P.eur, P.brl

INI_CORPO = R.CHEGADA[0]  # 10,10 s da fonte: "Acabamos de chegar aqui em Bruges"
FIM_CORPO = R.FIM_CORPO   # 882,55 s: "…não tem um defeito, venham demais."
TIMELAPSE = (736.71, 752.79, 4.0)  # REV4: 1 quadro para dentro de cada corte de cena (o fim encostava no plano seguinte)  # Marina soprando o waffle quente (corte de cena a corte de cena), 4× (pedido do Diego, 12:16)

# Janelas de música no corpo (fonte, s). As do vídeo mudo são exatamente as montagens de paisagem em que o Diego deixou o
# som em silêncio digital (medido em _tmp/voz_orig.wav, ≥ 1 s). Mais: o time-lapse e a cerveja no bar (sem fala).
# A faixa de cada seção (Biblioteca de áudio do YouTube; fonte/musica/, baixadas pelo Claude no Chrome a pedido do Diego).
# REV3 (Diego, 21/11/2026: "coloque músicas um pouco mais animadas, achei muito lentas"): as mais animadas do lote
# (rev3/musicas_animacao_rev3.json; escolha em rev3/MUSICA_REV3.md). Medidas da REV2 em rev2/musicas_medidas_rev2.json
FAIXA = {
    "G": "Bright Skies - Audio Hertz",
    "M1": "Top Of The Morning - TrackTribe",
    "M2": "Ripples In Time - Asher Fulero",
    "M3": "Swing Haven 1 - Los Angeles - Reed Mathis",
    "M4": "Starlight on the Water - Chris Haugen",
    "M5": "Peaked My Interest - Nathan Moore",
    "F": "Spring Migration - The Great North Sound Society",
}
# ponto da faixa (s) em que cada seção começa: pula as introduções calmas (curva de energia em rev2/musicas_medidas_rev2.json)
INICIO = {"G": 12.0, "M1": 1.0, "M2": 3.0, "M3": 0.0, "M4": 0.0, "M5": 9.0, "F": 15.0}

MUSICA = [
    ("M1", "Chegada e o primeiro waffle", "leve, curiosa, manhã: violão/ukulele, assobio ou pizzicato, 95–110 BPM", [(51.66, 72.16), (100.28, 118.76)]),
    ("M2", "Markt, Burg e canais: o conto de fadas", "encantadora e empolgante: cordas, celesta ou glockenspiel, pop orquestral leve, 100–120 BPM", [(147.53, 160.69), (214.11, 233.22), (271.96, 302.39), (343.55, 366.49)]),
    ("M3", "Fome, chocolate e a batata", "animada e gostosa: swing/jazz leve ou funk acústico, 105–120 BPM", [(458.35, 475.12), (497.94, 516.22), (604.97, 621.99)]),
    ("M4", "Minnewater: o descanso", "calma: piano ou violão dedilhado, lo-fi suave, 65–85 BPM", [(676.44, 696.71)]),
    ("M5", "O teste dos waffles e a despedida", "brincalhona/cômica: pizzicato, fagote, percussão leve, 100–120 BPM", [(696.71, 710.06), (TIMELAPSE[0], TIMELAPSE[1]), (816.55, 827.95)]),
]

# Legendas embutidas (pedido do Diego: "somente nesses pontos", falas com barulho). Fonte, s. O texto é o da
# transcrição (Whisper large-v3, palavra a palavra); na 3ª, o texto é o que o Diego disse que fala.
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

INSTAGRAM = [217.30, 459.00]  # 1ª ≈ 3 min (Markt, sem fala) e 2ª ≈ metade (canais, sem fala); a 3ª é a do fechamento
LIKE = 285.00  # versão curta, sem fala, ≈ 30% do vídeo: Basílica dourada (montagem do Burg)

FOTO_RELIQUIA = {"de": 389.00, "ate": 398.00, "arquivo": "basilica_reliquia_frasco.jpg", "x": 1250, "y": 110, "largura": 600, "altura": 398,
                 "foco": "50% 62%", "rotulo": "RELÍQUIA DO", "destino": "SANGUE SAGRADO", "credito": "foto: Matt Hopkins · CC BY-SA 2.0 · Wikimedia Commons"}
NOTA_HORARIO = {"de": 381.40, "dur": 4.6}  # REV2: entra no "nós temos sorte, a gente entrou era exatamente 12 horas", depois do corte da frase errada
BILHETE_WAFFLE = {"de": 696.80, "ate": 702.50}  # 11:36: "viemos dar uma chance para um novo waffle..."


def q(t):
    return round(t * FPS)


class Mapa:
    """Fonte (s) → vídeo final (ms) no corpo, pelos trechos mantidos da decupagem e o time-lapse."""

    def __init__(self, trechos):
        self.tr = trechos  # [{"src": ms, "de": ms, "ate": ms, "vel": v}]
        self.ini_src = [t["src"] for t in trechos]

    def ms(self, t):
        x = t * 1000
        i = bisect.bisect_right(self.ini_src, x) - 1
        i = max(0, min(i, len(self.tr) - 1))
        tr = self.tr[i]
        v = tr.get("vel", 1)
        fim_src = tr["src"] + (tr["ate"] - tr["de"]) * v
        if x > fim_src:  # caiu num corte: o instante seguinte que existe
            if i + 1 < len(self.tr):
                return self.tr[i + 1]["de"]
            return tr["ate"]
        return tr["de"] + (x - tr["src"]) / v


def trechos_corpo(G):
    edl = json.load(open("rev4/edl_rev4.json", encoding="utf-8"))
    assert edl["fps"] == FPS
    a0, a1 = q(INI_CORPO), q(FIM_CORPO)
    t0, t1, vel = q(TIMELAPSE[0]), q(TIMELAPSE[1]), TIMELAPSE[2]
    pedacos = []
    for qa, qb in edl["manter"]:
        qa, qb = max(qa, a0), min(qb, a1)
        if qb <= qa:
            continue
        # separa o time-lapse
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
    for a, b in zip(out, out[1:]):  # um grupo sai antes de o próximo entrar
        if a["fim"] > b["ini"] - 40:
            a["fim"] = b["ini"] - 40
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-guia", action="store_true", help="sem os textos de guia (narração a gravar e trechos de música)")
    a = ap.parse_args()

    # ---------------- gancho (o mesmo da prévia da narração) ----------------
    pg, trg, ng, G = P.props_gancho()
    ev = [e for e in pg["eventos"] if e["tipo"] != "guia"]
    gancho_tr = [t for t in trg if t["de"] < G]
    guias = [e for e in pg["eventos"] if e["tipo"] == "guia"]

    # ---------------- corpo ----------------
    corpo, B_fim, edl = trechos_corpo(G)
    mp = Mapa(corpo)
    ws = palavras()
    efeitos = []

    def ef(ms, nome, porque, dur=None):
        efeitos.append({"ms": ms, "nome": nome, "porque": porque, "dur": dur})

    ef(G + 500, "Placa \"1 DIA EM BRUGES →\" (Chegada + clack)", "Marca do vídeo (doc. do vídeo longo, seção 2) sobre a chegada na estação de Bruges", 3700)
    ef(G + 1000, "Data \"16 DE MARÇO DE 2026\" no painel do Placar", "Como em Bruxelas (pedido do Diego de 06/11/2026: a data quando o dia começa, nas cores do Placar)", 3600)
    t_rec_trem = [e for e in ev if e["tipo"] == "recibo"][0]["ini"]
    ef(t_rec_trem, "Recibo do trem: € 72,00 (€ 18 por trecho, por pessoa) + Placar 09:44", "Pedido do Diego: \"no vídeo da tela da compra da passagem, colocar que custou 18 euros por trecho por pessoa\". A tela da máquina mostra € 72,00", G - t_rec_trem)

    # mapa do trem
    t_m0, t_m1 = mp.ms(32.20), mp.ms(38.40)
    ev.append({"tipo": "mapa", "arquivo": "mapa_trem.json", "ini": t_m0, "fim": t_m1, "desenho": 2600})
    ef(t_m0, "Mapa Bruxelas → Bruges (Rota amarela se desenhando, Pin 1º em Bruges; whoosh + plim)", "Pedido do Diego: \"quando eu falo que a gente veio e durou 1 hora e pouquinho… coloca um mapinha\". Fala: \"a gente tem um trem… menos de uma hora de viagem… Foi uma hora\". Paradas com a hora dos clipes: Bruxelas 09:44 (compra do bilhete), Bruges 11:04 (chegada)", t_m1 - t_m0)

    # placar + recibos (o 1º gasto, o trem, já está no gancho)
    soma = sum(v for _, v in R.GASTOS[0]["linhas"])
    for g in R.GASTOS[1:]:
        t = mp.ms(g["t"])
        linhas = [(nome, VALOR_CA2 if v is None else v) for nome, v in g["linhas"]]
        nomes = [nome + (" (a confirmar)" if v is None else "") for nome, v in g["linhas"]]
        total = sum(v for _, v in linhas)
        antes = soma
        soma += total
        ev.append({"tipo": "placar", "ligar": t - 200, "desligar": t + 3400,
                   "valores": [{"em": t - 200, "tempo": g["hora"], "gasto": eur(antes)}, {"em": t + 400, "tempo": g["hora"], "gasto": eur(soma)}]})
        ev.append({"tipo": "recibo", "lugar": g["lugar"], "cabecalho": f"SEG 16/03 · {g['hora'].replace(':', 'H')} · BRUGES",
                   "linhas": [[n, eur(v)] for n, (_, v) in zip(nomes, linhas)], "total": eur(total), "real": "≈ " + brl(total * R.COTACAO),
                   "rodape": R.RODAPE, "ini": t, "fim": t + 5500, "x": 1400, "y": 150, "escala": 0.72})
        ef(t, f"Recibo {g['lugar']}: {eur(total)} + Placar {g['hora']} · {eur(soma)}", g["porque"], 5500)
    gastos_dia = round(soma, 2)

    # etiquetas de lugar
    for t_src, lugar, det in ETIQUETAS:
        t = mp.ms(t_src)
        ev.append({"tipo": "etiqueta", "lugar": lugar, "detalhe": det, "ini": t, "fim": t + DUR_ETIQUETA})
        ef(t, f"Etiqueta de lugar: {lugar} · {det}", "Lugar novo (doc. do vídeo longo: lugar + detalhe + hora; DS 5.4 lower third). Hora do arquivo no acervo", DUR_ETIQUETA)

    # relíquia (foto no canto) e nota do horário
    f = FOTO_RELIQUIA
    t0, t1 = mp.ms(f["de"]), mp.ms(f["ate"])
    ev.append({"tipo": "foto", "arquivo": f["arquivo"], "x": f["x"], "y": f["y"], "largura": f["largura"], "altura": f["altura"], "foco": f["foco"],
               "rotulo": f["rotulo"], "destino": f["destino"], "credito": f["credito"], "ini": t0, "fim": t1})
    ef(t0, "Foto da relíquia do Sangue Sagrado no canto direito (Placa + recorte de foto, DS 2.6) + placa P \"RELÍQUIA DO SANGUE SAGRADO\"",
       "Pedido do Diego: \"não pôde gravar o interior… colocar uma imagem meio escanteada… o cilindro que fica o sangue\". Entra no \"colocar à mostra o vidrinho lá que tem o sangue de Cristo\". Foto de Matt Hopkins, CC BY-SA 2.0 (crédito na tela e na descrição). Não cobre o rosto (x 1250–1850)", t1 - t0)
    t = mp.ms(NOTA_HORARIO["de"])
    ev.append({"tipo": "nota", "titulo": "horário da relíquia", "linhas": ["todo dia, das 14h às 16h", "(site oficial)"], "ini": t, "fim": t + NOTA_HORARIO["dur"] * 1000,
               "x": 1300, "y": 140, "largura": 520, "icone": "relogio"})
    ef(t, "Nota \"horário da relíquia: todo dia, das 14h às 16h (site oficial)\"", "Diego (21/11/2026): \"é 14 às 16, corrija minha frase\". A frase \"e ele fica exposto das 12 às 16 horas, e eu não sabia disso\" saiu da fala; o horário certo (holyblood.com) entra escrito no \"a gente entrou era exatamente 12 horas\"", NOTA_HORARIO["dur"] * 1000)

    # bilhete do novo waffle
    t0, t1 = mp.ms(BILHETE_WAFFLE["de"]), mp.ms(BILHETE_WAFFLE["ate"])
    ev.append({"tipo": "bilhete", "texto": "viemos dar uma chance|para um novo waffle...", "x": 1080, "y": 120, "escala": 0.85, "entrada": t0, "saida": t1})
    ef(t0, "Bilhete na letra de caneta: \"viemos dar uma chance para um novo waffle...\"", "Pedido do Diego: \"11:36 – coloque escrito na tela\". Bilhete = texto pessoal (DS 2.4), sobre a fachada da House of Waffles", t1 - t0)

    # time-lapse
    tl0, tl1 = mp.ms(TIMELAPSE[0]), mp.ms(TIMELAPSE[1] - 0.001)
    ev.append({"tipo": "nota", "titulo": "tá quente!", "linhas": ["esperando esfriar…", "4× mais rápido"], "ini": tl0 + 150, "fim": tl1 - 150, "x": 1290, "y": 140, "largura": 500, "icone": "relogio"})
    ev.append({"tipo": "som", "nome": "whoosh", "em": tl0, "relDb": -8})
    ef(tl0, "Time-lapse 4× da Marina soprando o waffle quente (16,2 s → 4,0 s) + nota \"tá quente! esperando esfriar… 4× mais rápido\" + whoosh na entrada",
       "Pedido do Diego: \"12:16 – Marina provando o waffle, coloque em time lapse com um efeito engraçado pq ela tá demorando e tá quente\". O som do trecho sai (acelerado vira voz de esquilo); entra a música M5", tl1 - tl0)

    # legendas
    cortes_src = [r["de_s"] for r in edl["removidos"]]
    leg = grupos_legenda(ws, mp, cortes_src)
    ev.append({"tipo": "legenda", "grupos": leg})
    for L in LEGENDAS:
        de = L["texto_fixo"][0][1] if "texto_fixo" in L else L["de"]
        ate = L["texto_fixo"][-1][2] if "texto_fixo" in L else L["ate"]
        ef(mp.ms(de), f"Legenda embutida que acende palavra a palavra (fonte {de:.1f}–{ate:.1f} s)", L["por"] + ". DS 3.4.2 (Barlow 700 56 px, x 960, base y 984) com a palavra amarela quando é dita e sem scrim (padrão de 19/11)", mp.ms(ate) - mp.ms(de))

    # instagram e like no corpo
    for t_src in INSTAGRAM:
        t = mp.ms(t_src)
        ev.append({"tipo": "instagram", "ini": t, "fim": t + 4000})
        ef(t, "Chamada SEGUE NO INSTAGRAM @primeirodiaem", "Doc. do vídeo longo: 3 vezes (≈ 2–3 min, ≈ metade, fechamento), em paisagem sem fala", 4000)
    t = mp.ms(LIKE)
    ev.append({"tipo": "like", "entrada": t, "saida": t + 3900})
    ef(t, "Animação \"DEIXA O LIKE E SE INSCREVE →\" (versão curta)", "Doc. do vídeo longo: 30–40% do vídeo, sobre uma montagem de paisagem sem fala", 3900)

    # ---------------- fechamento (o mesmo da prévia) ----------------
    pf, trf, nf, Fprev = P.props_fechamento()
    antes = 6000
    desloc = B_fim - antes  # a prévia começa 6 s antes do fechamento
    fech_tr = [dict(t, de=t["de"] + desloc, ate=t["ate"] + desloc) for t in trf[1:]]
    F_fim = Fprev + desloc
    for e in pf["eventos"]:
        e = json.loads(json.dumps(e))
        for k in ("ini", "fim", "entrada", "saida", "em", "inicio"):
            if k in e and isinstance(e[k], (int, float)):
                e[k] += desloc
        if e["tipo"] == "guia":
            for fr in e["frases"]:
                fr["ini"] += desloc
                fr["fim"] += desloc
            guias.append(e)
            continue
        ev.append(e)
    for n in nf:
        n["ini"] += desloc
        n["fim"] += desloc
    ef(B_fim, "Fechamento (narração F1–F7 a gravar) sobre as paisagens do dia", "Doc. do vídeo longo, seção 2. Recibo da viagem, Bilhete, nota da Basílica, like, Instagram, placa final, tela final", F_fim - B_fim)
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: paris →\")", "Ordem dos vlogs (CLAUDE.md, pendência 11)", TELA_FINAL)
    duracao = F_fim + TELA_FINAL

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
    # REV4: quadros congelados (câmera virando com a fala já começando): a imagem para num quadro bom e o som segue
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

    # janelas de música no relógio final
    janelas = []
    for mid, nome, clima, js in MUSICA:
        for s0, s1 in js:
            janelas.append({"id": mid, "nome": nome, "clima": clima, "ini": round(mp.ms(s0)), "fim": round(mp.ms(s1 - 0.001)), "fonte": [s0, s1]})
    janelas.append({"id": "G", "nome": "Abertura (gancho)", "clima": "empolgante, termina na compra do bilhete", "ini": 0, "fim": round(G), "fonte": None})
    janelas.append({"id": "F", "nome": "Fechamento e tela final", "clima": "nostálgica e quente", "ini": round(B_fim), "fim": round(duracao), "fonte": None})

    if not a.sem_guia:
        ev += guias
        frases = [{"ini": j["ini"], "fim": j["fim"], "texto": f"{j['id']} · {j['nome']} · ♪ {FAIXA[j['id']]}"} for j in janelas if j["id"].startswith("M")]
        ev.append({"tipo": "guia", "inicio": G, "fim": B_fim, "topo": True, "rotulo": "MÚSICA", "semContador": True, "frases": frases})

    props = {"video": P.VIDEO, "duracao": duracao, "fps": FPS, "trechos": trechos, "eventos": ev, "zooms": [], "refLufs": -16, "semGrao": True}
    json.dump(props, open("rev4/props_rev4.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"fps": FPS, "gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio,
               "narracoes": ng + nf, "musica": janelas, "faixas": FAIXA, "inicio_faixa_s": INICIO, "narracao_fim_gancho_ms": ng[-1]["fim"], "fechamento_narr_fim_ms": nf[-1]["fim"], "gastos_dia_previa": gastos_dia, "keen_ms": None},
              open("rev4/linha_do_tempo_rev4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---------------- relatórios ----------------
    def mmss(ms):
        s = ms / 1000
        return f"{int(s // 60)}:{s % 60:04.1f}".replace(".", ",")

    efeitos.sort(key=lambda e: e["ms"])
    with open("rev4/efeitos_rev4.md", "w", encoding="utf-8") as fh:
        fh.write("# REV4 · Efeitos e objetos (vlog de Bruges)\n\nTempos no vídeo final da REV4 (" + mmss(duracao) + "). Gerado por `rev4/montar_rev4.py`.\n\n")
        fh.write("| Entra | Dura | Efeito | Por quê |\n|---|---:|---|---|\n")
        for e in efeitos:
            fh.write(f"| {mmss(e['ms'])} | {'' if e['dur'] is None else f'{e[chr(100)+chr(117)+chr(114)] / 1000:.1f} s'.replace('.', ',')} | {e['nome']} | {e['porque']} |\n")
    with open("rev4/takes_rev4.md", "w", encoding="utf-8") as fh:
        fh.write("# REV4 · Takes do gancho e do fechamento (vlog de Bruges)\n\n| Bloco | No vídeo | Fonte | O que é |\n|---|---|---|---|\n")
        for t, tk in zip(gancho_tr, R.GANCHO):
            fh.write(f"| Gancho | {mmss(t['de'])}–{mmss(t['ate'])} ({(t['ate'] - t['de']) / 1000:.2f} s) | {tk['de']:.2f}–{tk['ate']:.2f} | {tk['o_que']} |\n")
        for t, tk in zip([t for t in fech_tr if not t.get("congela")], R.FECHAMENTO):
            fh.write(f"| Fechamento | {mmss(t['de'])}–{mmss(t['ate'])} ({(t['ate'] - t['de']) / 1000:.2f} s) | {tk['de']:.2f}–{tk['ate']:.2f} | {tk['o_que']} |\n")
    with open("rev4/musica_janelas_rev4.json", "w", encoding="utf-8") as fh:
        json.dump(janelas, fh, ensure_ascii=False, indent=1)
    print(f"gancho {mmss(G)} · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} · total {mmss(duracao)} · {len(trechos)} trechos · {len(ev)} eventos")
    for j in janelas:
        print(f"  {j['id']:>2} {mmss(j['ini'])}–{mmss(j['fim'])}  {j['nome']}")
    print(f"  legendas: {len(leg)} grupos; gastos do dia na prévia {eur(gastos_dia)}")


if __name__ == "__main__":
    main()
