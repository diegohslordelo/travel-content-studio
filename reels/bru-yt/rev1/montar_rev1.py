"""Montagem da REV1 do vlog de Bruxelas (vídeo longo do YouTube, 16:9, 30 fps). Modelo: Amsterdam REV3
(`reels/ams-yt/rev3/montar_rev3.py`), pelo passo a passo de `docs/VIDEO_LONGO_PASSO_A_PASSO.md`.

Pedidos do Diego (06/11/2026): notas de lugar e custo com o minuto da fonte; hotel no 4:50 com frase e imagens; nota do
waffle com os dois valores entrando em lista; gancho bem escolhido; decupagem sem comer palavra; mapas, motion
graphics e efeitos; cortes finais a partir de 14:22. As narrações (gancho, hotel e fechamento) ainda não foram
gravadas: esta revisão leva o texto na tela (`--guia`) para o Diego aprovar e gravar.

Escreve (de reels/bru-yt):  python rev1/montar_rev1.py [--guia]
  rev1/props_rev1.json            props da composição `VideoLongo` (Remotion), 30 fps
  rev1/linha_do_tempo_rev1.json   trechos de áudio para a mixagem (fonte → saída), narrações e totais
  rev1/efeitos_rev1.md            cada efeito: minuto em que entra e por quê
  rev1/takes_rev1.md              os takes do gancho e do fechamento

Valores: registro do Diego (06/11/2026). Real ↔ euro pela PTAX de venda do Banco Central de 13/03/2026 (último dia útil
antes de 15/03/2026, domingo, o dia em Bruxelas): € 1 = R$ 6,0128.
"""
import argparse
import json
import sys
from bisect import bisect_right
from decimal import ROUND_HALF_UP, Decimal

FPS = 30
COTACAO = 6.0128
RODAPE = "cotação € 1 = R$ 6,0128 · PTAX 13/03/2026"
TELA_FINAL = 20000
DUR_PAGINA = 700
MIN_TAKE = 2.0
FIM_CORPO = 862.20  # a partir de 14:22,2 da fonte entram os "cortes finais" (Grand Place à noite): viram o fechamento
HOTEL_BRL = 1738.78  # ibis Brussels off Grand Place, 2 noites, 2 pessoas (Diego, 06/11/2026)
NOITES_NO_DIA = 1  # [DECISÃO A CONFIRMAR] o total de Bruxelas leva 1 das 2 noites; a outra é do bate-volta a Bruges
BILHETE_EUR = 18.00  # [A CONFIRMAR] bilhete diário, "18 euros por pessoa" (Diego); a STIB anuncia o de 24 h por ≈ € 7,50–8,70


def s(t):
    """'m:ss.s' ou segundos → segundos."""
    if isinstance(t, (int, float)):
        return float(t)
    m, r = t.split(":")
    return int(m) * 60 + float(r)


def _fmt(v):
    v = Decimal(str(round(v, 6))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def eur(v):
    return "€ " + _fmt(v)


def brl(v):
    return "R$ " + _fmt(v)


def real(v):
    return "≈ " + brl(v * COTACAO)


# cortes de cena da fonte (ffmpeg scene > 0,22; _tmp/cenas.json), só os que cercam os takes
CENAS = [27.07, 29.73, 33.07, 36.57, 43.70, 46.33, 108.33, 111.43, 115.23, 119.07, 132.37, 140.67, 167.77, 181.00, 183.70,
         203.00, 208.03, 212.30, 215.23, 217.93, 222.37, 226.27, 290.80, 294.17, 296.57, 298.73, 302.00, 304.50, 307.50, 325.73,
         328.47, 331.37, 334.37, 421.20, 426.40, 429.83, 433.10, 447.07, 463.03, 528.17, 531.10, 534.00, 537.93, 540.00, 543.17,
         546.50, 550.10, 554.77, 557.43, 608.87, 618.53, 623.40, 627.00, 673.90, 676.37, 678.47, 680.83, 684.33, 787.17, 790.33,
         796.30, 798.37, 802.57, 862.23]

# ------------------------------------------------------------------------------------------------
# GANCHO (fonte em s). `aud` (opcional): de onde vem o som do take, quando não é o da própria imagem (J-cut dos ovos).
GANCHO = [
    {"de": 108.55, "ate": 111.25, "o_que": "Atomium de baixo para cima, céu azul (12h19)", "som": "baixo"},
    {"de": 134.75, "ate": 139.45, "o_que": "Zinneke: \"Ponto turístico de Bruxelas… Um cachorro mijando.\"", "som": "fala"},
    {"de": 181.05, "ate": 183.60, "o_que": "batata e sanduíche da Fritland (close)", "som": "baixo"},
    {"de": 331.45, "ate": 334.30, "o_que": "waffle com Nutella do Le Roi de la Gaufre (close)", "som": "baixo"},
    {"de": 426.50, "ate": 429.75, "aud": 447.10, "o_que": "vitrine dos ovos de Páscoa (Galerias), com o som de \"seis ovos de páscoa, menores que meu dedo…\"", "som": "fala"},
    {"de": 450.35, "ate": 453.15, "o_que": "Diego: \"…estão a 26 euros pela vitrine.\"", "som": "fala"},
    {"de": 454.95, "ate": 457.00, "o_que": "Diego: \"Não tem condições.\"", "som": "fala"},
    {"de": 218.05, "ate": 221.55, "o_que": "chegada na Grand Place (dia)", "som": "baixo"},
    {"de": 862.30, "ate": 865.30, "o_que": "Grand Place à noite", "som": "baixo"},
]
# narrações a gravar: onde a fala começa (ms no relógio do bloco), duração prevista (ms) e o texto
NARRACAO_GANCHO = [
    {"id": "G1", "em": 250, "dur": 2300, "texto": "Quanto custa um dia inteiro em Bruxelas?"},
    {"id": "G2", "em": 7650, "dur": 4300, "texto": "Batata frita, waffle… e um chocolate que a gente não teve coragem de comprar:"},
    {"id": "G3", "em": 20550, "dur": 6200, "texto": "Eu anotei cada euro que a gente gastou. No final, eu te mostro quanto deu o dia todo, e se vale a pena."},
]

# HOTEL (pedido do Diego: no 4:50 da fonte, sobre a montagem das fachadas da Grand Place, antes da Jeanneke Pis)
NARRACAO_HOTEL = {"id": "H1", "src": 291.20, "dur": 14300,
                  "texto": "Falando em hotel: a gente ficou no ibis Brussels off Grand Place, a uns 200 metros da praça. Foi o mais barato que achamos no centro, e com um dia só, ficar perto de tudo fez diferença. Foram duas noites, uma pra Bruxelas e outra pro bate-volta em Bruges: 1.738 reais para o casal."}

# FECHAMENTO: planos sem fala depois do último plano falado (14:21) + paisagens do dia
FECHAMENTO = [
    {"de": 862.25, "ate": 867.25, "o_que": "Grand Place à noite (os \"cortes finais\" do Diego, 14:22)"},
    {"de": 790.40, "ate": 796.25, "o_que": "Boulevard Anspach na hora azul"},
    {"de": 618.60, "ate": 623.35, "o_que": "jardim do Mont des Arts no fim da tarde"},
    {"de": 623.45, "ate": 626.95, "o_que": "Mont des Arts com o sol baixo"},
    {"de": 550.15, "ate": 554.70, "o_que": "Praça Real (Saint-Jacques-sur-Coudenberg)"},
    {"de": 421.25, "ate": 426.35, "o_que": "Galerias Reais Saint-Hubert"},
    {"de": 111.50, "ate": 115.20, "o_que": "Atomium de longe"},
    {"de": 678.50, "ate": 680.80, "o_que": "vitrine do Aux Merveilleux de Fred"},
    {"de": 215.28, "ate": 217.90, "o_que": "Bolsa de Bruxelas (Bourse)"},
    {"de": 290.85, "ate": 294.15, "o_que": "fachadas douradas da Grand Place"},
    {"de": 298.75, "ate": 301.95, "o_que": "torre da Prefeitura na Grand Place"},
]
NARRACAO_FECHAMENTO = [
    {"id": "F1", "em": 1200, "dur": 5900, "texto": "Num dia só, a gente rodou Bruxelas inteira: do Atomium à Grand Place, passando pelas três estátuas que fazem xixi."},
    {"id": "F2", "em": 7600, "dur": 5400, "texto": "Metrô, comida, cerveja e doce: o dia deu {gastos} euros para nós dois."},
    {"id": "F3", "em": 13700, "dur": 7000, "texto": "Somando uma noite de hotel, ficou em uns {total} euros: {pp} por pessoa, perto de {pp_brl} reais."},
    {"id": "F4", "em": 21300, "dur": 5800, "texto": "Vale a pena? Muito. Mas leve luva e casaco: o sol engana, e o vento não perdoa."},
    {"id": "F5", "em": 27700, "dur": 6600, "texto": "Se esse vídeo te ajudou, se inscreve, deixa o like aqui e me segue no Instagram: @primeirodiaem."},
    {"id": "F6", "em": 34900, "dur": 5600, "texto": "Toda cidade tem um primeiro dia. E o próximo é em Bruges, de bate-volta. Te espero lá!"},
]

# GASTOS (fonte em s; valores do Diego, 06/11/2026). hora = relógio do clipe na tela (hora do arquivo no acervo).
GASTOS = [
    {"t": 33.10, "lugar": "METRÔ · STIB", "hora": "12:15", "linhas": [("Bilhete diário × 2", 2 * BILHETE_EUR)], "cat": "transporte",
     "porque": "Diego: 00:33, compra do bilhete diário do transporte público, 18 euros por pessoa. Entra no 1º plano depois do metrô (saída no Heysel, 12h15)"},
    {"t": 181.20, "lugar": "FRITLAND", "hora": "13:53", "linhas": [("Sanduíche com fritas", 9.00)],
     "porque": "Diego: 03:01, 9 euros; na fala, \"um sanduíche de batata frita… tem carne também, a gente vai dividir\". Entra no close do sanduíche"},
    {"t": 361.50, "lugar": "LE ROI DE LA GAUFRE", "hora": "14:36", "linhas": [("Waffle simples", 3.50), ("Waffle + Nutella", 5.00)],
     "aparecer": [0.0, 366.20 - 361.50],
     "porque": "Diego: 06:02 \"o meu foi 3,5 euros\" e 06:08 \"o dela foi 5 euros\", aparecendo aos poucos na nota, em lista. Cada linha entra quando o valor é falado (6:01,5 e 6:06,2), com a moeda"},
    {"t": 668.20, "lugar": "BRASSERIE DE LA MADELEINE", "hora": "17:57", "linhas": [("2 cervejas", 6.20)],
     "porque": "Diego: 11:11, 6,20 euros, duas cervejas. Entra 2,8 s antes (11:08,2), para sair antes do corte para o Aux Merveilleux (11:13,9)"},
    {"t": 700.00, "lugar": "AUX MERVEILLEUX DE FRED", "hora": "18:38", "linhas": [("Pão + merveilleux", 8.50)],
     "porque": "Diego: 11:40, os dois deu 8,50. Entra quando ele mostra os dois doces (\"um pão de chocolate e… um bolinho de chocolate branco\")"},
    {"t": 834.30, "lugar": "SPAGO RISTORANTE", "hora": "20:27", "linhas": [("Pizza, cerveja e Coca", 25.90)],
     "porque": "Diego: 13:55, 25,90 euros. Na fala ele arredonda (\"a conta deu 25 euros\"); o Recibo mostra o valor do registro. Entra no \"25\" (13:54,3)"},
]

# ETIQUETAS DE LUGAR (lower third): lugar, rua/bairro (OpenStreetMap ou GPS do clipe no acervo) e hora do arquivo
ETIQUETAS = [
    (46.60, "ATOMIUM", "HEYSEL · 12H16"),
    (132.50, "ZINNEKE PIS", "RUE DES CHARTREUX · 13H16"),
    (168.20, "FRITLAND", "RUE HENRI MAUS · 13H53"),
    (215.40, "BOLSA DE BRUXELAS", "BOULEVARD ANSPACH · 14H07"),
    (223.00, "GRAND PLACE", "PATRIMÔNIO DA UNESCO · 14H10"),
    (307.70, "JEANNEKE PIS", "IMPASSE DE LA FIDÉLITÉ · 14H24"),
    (325.90, "LE ROI DE LA GAUFRE", "RUE DE LA FOURCHE · 14H36"),
    (390.00, "GALERIAS REAIS SAINT-HUBERT", "DESDE 1847 · 14H49"),
    (468.10, "MANNEKEN PIS", "RUE DE L'ÉTUVE · 16H12"),
    (534.20, "MONT DES ARTS", "BAIRRO REAL · 16H33"),
    (550.20, "PRAÇA REAL", "PLACE ROYALE · 16H34"),
    (651.20, "BRASSERIE DE LA MADELEINE", "GALERIE BORTIER · 17H57"),
    (674.10, "AUX MERVEILLEUX DE FRED", "PETITE RUE AU BEURRE · 18H38"),
    (796.40, "SPAGO RISTORANTE", "RUE DU PONT DE LA CARPE · 20H00"),
]
DUR_ETIQUETA = {}

# NOTAS (camada de efeitos; fatos externos conferidos na web em 06/11/2026, fontes na QA)
NOTAS = [
    {"t": 82.40, "dur": 7.0, "titulo": "Sabia?", "linhas": ["Um cristal de ferro", "ampliado 165 bilhões de vezes.", "Feito para a Expo 58."], "x": 1252, "y": 150, "largura": 580, "cor": "#3DA9FC", "cor2": "#8B5CF6", "icone": "dica",
     "porque": "A Marina fala (1:22–1:34). Site oficial do Atomium: cristal elementar de ferro ampliado 165 bilhões de vezes; construído para a Expo 58"},
    {"t": 141.00, "dur": 6.0, "titulo": "Zinneke = vira-lata", "linhas": ["Em dialeto de Bruxelas.", "Estátua de Tom Frantzen,", "sem água: é só bronze."], "x": 1292, "y": 150, "largura": 540, "cor": "#18C6B3", "cor2": "#3DA9FC", "icone": "dica",
     "porque": "Visit Brussels e Wikipédia: \"zinneke\" é vira-lata no dialeto local; obra de Tom Frantzen; ao contrário dos outros dois, não é fonte"},
    {"t": 187.00, "dur": 6.0, "titulo": "Tem nome: mitraillette", "linhas": ["Baguete com carne, fritas", "e molho: clássico", "das friteries de Bruxelas."], "x": 1292, "y": 150, "largura": 560, "cor": "#FF9F1C", "cor2": "#FF5A4E", "icone": "dica",
     "porque": "O sanduíche que eles dividiram é baguete com carne e fritas, o que na Bélgica se chama mitraillette (Wikipédia, Beer City Brussels)"},
    {"t": 446.60, "dur": 7.5, "titulo": "Na vitrine", "linhas": ["6 ovinhos de Páscoa:", "€ 26", "(a gente não comprou)"], "x": 1292, "y": 470, "largura": 520, "cor": "#FF5A4E", "cor2": "#FF4FA3", "icone": "alerta",
     "porque": "Diego (7:26): \"seis ovos de páscoa, menores que meu dedo, estão a 26 euros pela vitrine\". Não é gasto: fica fora do Placar"},
    {"t": 493.00, "dur": 6.5, "titulo": "1.141 roupas", "linhas": ["É o guarda-roupa do", "Manneken Pis (fim de 2023).", "Hoje: jogador de futebol."], "x": 1272, "y": 150, "largura": 560, "cor": "#8B5CF6", "cor2": "#FF4FA3", "icone": "dica",
     "porque": "Diego fala que vestem o menino. Regulamento da cidade de Bruxelas (2025): 1.141 trajes no fim de 2023"},
    {"t": 741.90, "dur": 6.0, "titulo": "Merveilleux", "linhas": ["Suspiro com chantili,", "coberto de raspas", "de chocolate."], "x": 1292, "y": 150, "largura": 520, "cor": "#FF4FA3", "cor2": "#8B5CF6", "icone": "dica",
     "porque": "A Marina descobre o recheio (12:08–12:22). Merveilleux: camadas de suspiro e chantili cobertas de chocolate (Time Out, David Lebovitz)"},
    {"t": 771.80, "dur": 5.0, "titulo": "7 °C", "linhas": ["com vento:", "leve luva!"], "x": 1352, "y": 410, "largura": 440, "cor": "#3DA9FC", "cor2": "#8B5CF6", "icone": "alerta",
     "porque": "A Marina: \"tá marcando 7 graus\" (12:51); o Diego comprou uma luva para ela"},
]

# MAPAS (public/mapa_*.json, gerados por scripts/mapa_osm.py a partir do OpenStreetMap)
MAPAS = [
    {"t": 29.80, "ate": 33.05, "arquivo": "mapa_centro_atomium.json", "desenho": 1700, "o_que": "do centro ao Atomium, de metrô",
     "porque": "Deslocamento longo (≈ 6 km) que o vídeo não mostra: entre a rua do centro e a saída do metrô no Heysel"},
    {"t": 115.30, "ate": 119.00, "arquivo": "mapa_atomium_zinneke.json", "desenho": 2000, "o_que": "do Atomium ao Zinneke Pis, de metrô",
     "porque": "Volta ao centro: entra na rua que leva ao Zinneke, depois dos planos do Atomium"},
    {"t": 531.15, "ate": 534.00, "arquivo": "mapa_manneken_praca_real.json", "desenho": 1500, "o_que": "do Manneken Pis ao Mont des Arts e à Praça Real, a pé",
     "porque": "A subida para o bairro real (o Diego: \"uma das regiões… um pouco mais alta\")"},
]


class Mapa:
    """Fonte (s) → saída (ms) pela decupagem; o corpo começa em `base` ms."""

    def __init__(self, manter, base):
        self.seg = manter
        self.base = base
        self.ini_src = [a / FPS for a, _ in self.seg]
        acc = 0
        self.ini_out = []
        for a, b in self.seg:
            self.ini_out.append(acc)
            acc += b - a
        self.dur_q = acc

    def ms(self, t):
        t = s(t)
        i = bisect_right(self.ini_src, t) - 1
        if i < 0:
            return self.base
        a, b = self.seg[i]
        if t * FPS >= b:
            i = min(i + 1, len(self.seg) - 1)
            return self.base + self.ini_out[i] * 1000 / FPS
        return self.base + (self.ini_out[i] + (t * FPS - a)) * 1000 / FPS


def confere_takes(lista, nome):
    for c in lista:
        dur = c["ate"] - c["de"]
        assert dur >= MIN_TAKE - 1e-6, f"{nome}: take de {dur:.2f} s ({c['o_que']})"
        dentro = [x for x in CENAS if c["de"] + 0.02 < x < c["ate"] - 0.02]
        assert not dentro, f"{nome}: corte de cena em {dentro} dentro do take {c['o_que']}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guia", action="store_true")
    a = ap.parse_args()
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))
    confere_takes(GANCHO, "gancho")
    confere_takes(FECHAMENTO, "fechamento")
    q = lambda ms: round(ms * FPS / 1000)  # noqa: E731
    trechos, audio, efeitos, takes = [], [], [], []

    def ef(ms, nome, porque, dur=None):
        efeitos.append({"ms": ms, "nome": nome, "porque": porque, "dur": dur})

    # ---------- gancho ----------
    pos = 0
    for c in GANCHO:
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        trechos.append({"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur})
        audio.append({"src": c.get("aud", c["de"]), "out": pos, "dur": dur, "tipo": "gancho_" + c["som"]})
        takes.append(("gancho", pos, dur, c))
        pos += dur
    G = pos

    # ---------- corpo (decupado, até FIM_CORPO) ----------
    q_fim = round(FIM_CORPO * FPS)
    manter = [[x, min(y, q_fim)] for x, y in edl["manter"] if x < q_fim]
    mp = Mapa(manter, G)
    for (qa, qb), out0 in zip(manter, mp.ini_out):
        de = G + out0 * 1000 / FPS
        ate = G + (out0 + qb - qa) * 1000 / FPS
        trechos.append({"src": round(qa * 1000 / FPS), "de": de, "ate": ate})
        audio.append({"src": qa / FPS, "out": de, "dur": ate - de, "tipo": "corpo"})
    B_fim = G + mp.dur_q * 1000 / FPS

    # ---------- fechamento ----------
    pos = B_fim
    for i, c in enumerate(FECHAMENTO):
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        tr_ = {"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur}
        if i == len(FECHAMENTO) - 1:
            tr_["pagina"] = True
        trechos.append(tr_)
        audio.append({"src": c["de"], "out": pos, "dur": dur, "tipo": "fechamento"})
        takes.append(("fechamento", pos, dur, c))
        pos += dur
    F_fim = pos
    duracao = F_fim + TELA_FINAL
    ev, zooms = [], []
    REF = -16

    # ---------- marca ----------
    ev.append({"tipo": "placa", "rotulo": "1 DIA EM", "destino": "BRUXELAS", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": G + 500, "saida": G + 4200})
    ef(G + 500, "Placa \"1 DIA EM BRUXELAS →\" (Chegada + clack)", "Marca do vídeo (doc. do vídeo longo, seção 2), sobre o \"Bom dia, Bélgica!\". Sem placa de capítulo \"DIA 1\": o vídeo tem um dia só", 3700)

    # ---------- placar + recibos ----------
    def valor(g):
        return sum(v for _, v in g["linhas"])

    aparicoes, soma = [], 0.0
    for gst in sorted(GASTOS, key=lambda g: g["t"]):
        t_rec = mp.ms(gst["t"])
        passos = [t_rec + 1000 * x for x in gst.get("aparecer", [0.0])] if "aparecer" in gst else [t_rec]
        valores_passo = [v for _, v in gst["linhas"]] if "aparecer" in gst else [valor(gst)]
        for k, (tp, vp) in enumerate(zip(passos, valores_passo)):
            em = tp + 400
            antes = soma
            soma += vp
            if aparicoes and tp - 200 <= aparicoes[-1]["desligar"] + 2500:
                aparicoes[-1]["valores"].append({"em": em, "tempo": gst["hora"], "gasto": eur(round(soma, 2))})
                aparicoes[-1]["desligar"] = em + 3000
                if gst["lugar"] not in aparicoes[-1]["lugares"]:
                    aparicoes[-1]["lugares"].append(gst["lugar"])
            else:
                aparicoes.append({"ligar": tp - 200, "desligar": em + 3000, "lugares": [gst["lugar"]],
                                  "valores": [{"em": tp - 200, "tempo": gst["hora"], "gasto": eur(round(antes, 2))}, {"em": em, "tempo": gst["hora"], "gasto": eur(round(soma, 2))}]})
    for ap_ in aparicoes:
        ev.append({"tipo": "placar", "valores": ap_["valores"], "ligar": ap_["ligar"], "desligar": ap_["desligar"]})
        ef(ap_["ligar"], f"Placar: {ap_['valores'][0]['tempo']} · {ap_['valores'][-1]['gasto']} ({', '.join(ap_['lugares'])})",
           "Regra do vlog de Amsterdam (Diego, 23/10/2026): só aparece quando um gasto é somado, com a hora real do clipe; liga sem som (a moeda é a do Recibo), soma e apaga 3 s depois", ap_["desligar"] - ap_["ligar"])
    total_gastos = round(soma, 2)

    for gst in GASTOS:
        t = mp.ms(gst["t"])
        total = valor(gst)
        h, m = gst["hora"].split(":")
        r = {"tipo": "recibo", "lugar": gst["lugar"], "cabecalho": f"DOM 15/03 · {h}H{m} · BRUXELAS", "linhas": [[it, eur(v)] for it, v in gst["linhas"]],
             "total": eur(total), "real": real(total), "rodape": RODAPE, "ini": t, "fim": t + 5500, "x": 1400, "y": 150, "escala": 0.72}
        if "aparecer" in gst:
            acum = 0.0
            r["aparecer"] = [round(1000 * x) for x in gst["aparecer"]]
            r["totais"] = []
            for _, v in gst["linhas"]:
                acum += v
                r["totais"].append({"total": eur(acum), "real": real(acum)})
            r["fim"] = t + r["aparecer"][-1] + 5000
        ev.append(r)
        ef(t, f"Recibo {gst['lugar']}: {eur(total)} (máquina de moeda" + (", uma por linha)" if "aparecer" in gst else ")"), gst["porque"], r["fim"] - t)

    # ---------- etiquetas de lugar ----------
    for t, lugar, det in ETIQUETAS:
        ini = mp.ms(t)
        dur = DUR_ETIQUETA.get(lugar, 4.0) * 1000
        ev.append({"tipo": "etiqueta", "lugar": lugar, "detalhe": det, "ini": ini, "fim": ini + dur})
        ef(ini, f"Etiqueta de lugar: {lugar} · {det}", "Lugar novo (doc., seção 2: lugar + rua/bairro + hora; DS 5.4 lower third). Rua pelo OpenStreetMap e pelo GPS do clipe no acervo; hora do arquivo", dur)

    # ---------- hotel (narração H1 + print + Recibo da hospedagem) ----------
    h0 = mp.ms(NARRACAO_HOTEL["src"])
    hotel_eur = HOTEL_BRL / COTACAO
    t_print, fim_print = h0 + 1700, h0 + 9300
    ev.append({"tipo": "print", "arquivo": "print_hotel_PENDENTE.png", "endereco": "booking.com · ibis Brussels off Grand Place", "ini": t_print, "fim": fim_print, "x": 820, "y": 110, "largura": 1000, "alturaJanela": 560, "rolagem": 0})
    ef(t_print, "Print da página do hotel (janela de navegador) — ESPAÇO RESERVADO até o print do Diego", "Pedido do Diego: imagens da fachada e do quarto do Booking/Hoteis.com no 4:50, que não foi gravado. Componente do vlog de Amsterdam (print do Hoteis.com)", fim_print - t_print)
    t_rh = fim_print + 250
    ev.append({"tipo": "recibo", "lugar": "IBIS OFF GRAND PLACE", "cabecalho": "HOSPEDAGEM · 2 NOITES · 2 PESSOAS", "linhas": [["2 noites", brl(HOTEL_BRL)], ["por noite", brl(HOTEL_BRL / 2)]],
               "total": eur(hotel_eur), "real": f"pago {brl(HOTEL_BRL)}", "rodape": RODAPE, "ini": t_rh, "fim": h0 + NARRACAO_HOTEL["dur"] + 900, "x": 1400, "y": 150, "escala": 0.72})
    ef(t_rh, f"Recibo da hospedagem: {brl(HOTEL_BRL)} = {eur(hotel_eur)} (2 noites)", "Diego: R$ 1.738,78 para duas pessoas e duas noites. Fica fora do Placar do dia (é a estadia; regra de Amsterdam) e entra no total do fechamento", None)

    # ---------- notas, bilhete, ticket ----------
    for n in NOTAS:
        t = mp.ms(n["t"])
        ev.append({"tipo": "nota", "titulo": n["titulo"], "linhas": n["linhas"], "ini": t, "fim": t + n["dur"] * 1000, "x": n["x"], "y": n["y"], "largura": n["largura"], "cor": n["cor"], "cor2": n["cor2"], "icone": n["icone"]})
        ef(t, f"Nota \"{n['titulo']}\": {' '.join(n['linhas'])}", n["porque"], n["dur"] * 1000)
    t = mp.ms(357.10)
    ev.append({"tipo": "bilhete", "texto": "extremamente|aprovado!", "marca": "vale", "x": 1240, "y": 560, "escala": 0.8, "entrada": t, "saida": t + 3200})
    ef(t, "Bilhete na letra do Diego: \"extremamente aprovado!\" + ✓", "O Diego diz \"Extremamente aprovado\" (5:57): opinião vira Bilhete (DS 2.4)", 3400)
    t = mp.ms(576.40)
    ev.append({"tipo": "ticket", "variante": "vale", "palavra": "VALE A PENA", "micro": "MONT DES ARTS · FIM DE TARDE", "x": 1250, "y": 760, "escala": 0.72, "entrada": t, "saida": t + 4200})
    ef(t, "Selo VALE A PENA (Ticket VALE, Subida + ding)", "O Diego: \"vale muito a pena vir aqui, principalmente nesse período de final de tarde\" (9:36)", 4440)

    # ---------- mapas ----------
    for mm in MAPAS:
        ini, fim = mp.ms(mm["t"]), mp.ms(mm["ate"])
        ev.append({"tipo": "mapa", "arquivo": mm["arquivo"], "ini": ini, "fim": fim, "desenho": mm["desenho"]})
        ef(ini, f"Mapa: {mm['o_que']} (Rota amarela se desenhando + Pin 1º; whoosh + plim)", mm["porque"] + ". Base OpenStreetMap (tiles vetoriais), cores naturais do DS 2.3.0", fim - ini + 240)

    # ---------- chamadas ----------
    for t, dur, porque in [(203.30, 4.5, "1ª de 3 (≈ 3 min): planos da Fritland, sem fala"), (521.20, 4.5, "2ª de 3 (≈ metade do vídeo): multidão no Manneken Pis, sem fala")]:
        ini = mp.ms(t)
        ev.append({"tipo": "instagram", "ini": ini, "fim": ini + dur * 1000})
        ef(ini, "Chamada SEGUE NO INSTAGRAM @primeirodiaem", porque, dur * 1000)
    t = mp.ms(330.30)
    ev.append({"tipo": "like", "entrada": t, "saida": t + 3900})
    ef(t, "Animação \"DEIXA O LIKE E SE INSCREVE\" (clique + ding)", "Doc., seção 2: versão curta, sem fala, em 30–40% do vídeo: dentro do Le Roi de la Gaufre, antes do waffle", 4140)

    # ---------- fechamento ----------
    f = B_fim
    noite = hotel_eur / 2
    hotel_dia = noite * NOITES_NO_DIA
    total = total_gastos + hotel_dia
    pp = total / 2
    cat = {"comida": 0.0, "transporte": 0.0}
    for g in GASTOS:
        cat[g.get("cat", "comida")] += valor(g)
    assert abs(sum(cat.values()) - total_gastos) < 0.005
    ev.append({"tipo": "mapa", "arquivo": "mapa_dia_centro.json", "ini": f + 3800, "fim": f + 10300, "desenho": 4200})
    ef(f + 3800, "Mapa do dia no centro (9 paradas, da Zinneke ao Spago)", "Fechamento (F1): o roteiro inteiro a pé, depois do Atomium. Entra depois de 3,8 s da Grand Place à noite (os \"cortes finais\" do Diego abrem o fechamento com a música)", 6740)
    ev.append({"tipo": "recibo", "lugar": "1 DIA EM BRUXELAS", "cabecalho": "DOM 15/03 · 2 PESSOAS · SEM PASSAGEM", "linhas": [["Comida e bebida", eur(cat["comida"])], ["Metrô", eur(cat["transporte"])], ["Hotel (1 noite)", eur(hotel_dia)]],
               "total": eur(total), "real": f"{eur(pp)} por pessoa ≈ {brl(pp * COTACAO)}", "rodape": RODAPE, "ini": f + 10600, "fim": f + 21000, "x": 1360, "y": 96, "escala": 0.78,
               "aparecer": [0, 0, 3500], "totais": [{"total": eur(total_gastos), "real": f"{eur(total_gastos / 2)} por pessoa"}, {"total": eur(total_gastos), "real": f"{eur(total_gastos / 2)} por pessoa"}, {"total": eur(total), "real": f"{eur(pp)} por pessoa ≈ {brl(pp * COTACAO)}"}]})
    ef(f + 10600, f"Recibo do dia: {eur(total_gastos)} sem hotel → {eur(total)} com 1 noite ({eur(pp)} por pessoa)", "Doc., seção 2: total (2 pessoas e por pessoa, € e R$). Responde à pergunta do gancho. A linha do hotel entra com o F3 (\"Somando uma noite de hotel\")", 10400)
    ev.append({"tipo": "bilhete", "texto": "vale muito!|leve luva", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": f + 22300, "saida": f + 26900})
    ef(f + 22300, "Bilhete do veredito: \"vale muito! leve luva\" + ✓", "Doc., seção 2: Bilhete com o veredito (F4)", 4900)
    ev.append({"tipo": "like", "entrada": f + 29100, "saida": f + 32100})
    ef(f + 29100, "Animação \"DEIXA O LIKE E SE INSCREVE\" (2ª vez)", "No \"se inscreve, deixa o like aqui\" (F5)", 3240)
    ev.append({"tipo": "instagram", "ini": f + 32200, "fim": f + 34700})
    ef(f + 32200, "Chamada SEGUE NO INSTAGRAM (3ª vez)", "No \"me segue no Instagram: @primeirodiaem\" (F5)", 2600)
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": f + 34900, "saida": F_fim - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": f + 34900 + 400, "relDb": -12})
    ef(f + 34900, "Placa de fechamento \"TODA CIDADE TEM UM PRIMEIRO DIA.\" + Nascer do 1º", "DS 4.3 e 5.4 (aprovada em Amsterdam, 23/10/2026), no F6", F_fim - f - 34900)
    ev.append({"tipo": "telafinal", "ini": F_fim, "proximo": "bruges"})
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: bruges →\")", "Doc., seção 2. Ordem dos vlogs (CLAUDE.md, pendência 11): Amsterdam, Bruxelas, Bruges…", TELA_FINAL)

    # narrações no relógio do vídeo final
    fmt = {"gastos": f"{total_gastos:.0f}", "total": f"{total:.0f}", "pp": f"{pp:.0f}", "pp_brl": f"{round(pp * COTACAO, -1):.0f}"}
    narr = []
    for base, lista in [(0, NARRACAO_GANCHO), (B_fim, NARRACAO_FECHAMENTO)]:
        for n in lista:
            narr.append({"id": n["id"], "arq": f"{n['id']}.m4a", "fala_ini": base + n["em"], "fala_fim": base + n["em"] + n["dur"], "texto": n["texto"].format(**fmt)})
    narr.append({"id": "H1", "arq": "H1.m4a", "fala_ini": h0, "fala_fim": h0 + NARRACAO_HOTEL["dur"], "texto": NARRACAO_HOTEL["texto"]})
    narr.sort(key=lambda n: n["fala_ini"])
    for a_, b_ in zip(narr, narr[1:]):
        assert a_["fala_fim"] + 150 <= b_["fala_ini"], (a_["id"], b_["id"])
    assert mp.ms(307.50) >= h0 + NARRACAO_HOTEL["dur"], "a narração do hotel passa da Jeanneke Pis"
    assert narr[-1]["fala_fim"] < F_fim - 300

    if a.guia:
        frases = [{"ini": n["fala_ini"], "fim": n["fala_fim"], "texto": f"{n['id']} · {n['texto']}"} for n in narr]
        ev.append({"tipo": "guia", "inicio": 0, "fim": G, "frases": frases})
        ev.append({"tipo": "guia", "inicio": h0 - 1500, "fim": h0 + NARRACAO_HOTEL["dur"] + 1500, "frases": frases})
        ev.append({"tipo": "guia", "inicio": B_fim, "fim": F_fim, "topo": True, "frases": frases})

    props = {"video": "http://127.0.0.1:8787/proxy1080.mp4", "duracao": duracao, "fps": FPS, "trechos": trechos, "eventos": ev, "zooms": zooms, "refLufs": REF}
    sufixo = "_guia" if a.guia else ""
    json.dump(props, open(f"rev1/props_rev1{sufixo}.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"fps": FPS, "gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio, "narracoes": narr,
               "hotel_ms": [h0, h0 + NARRACAO_HOTEL["dur"]], "manter": manter,
               "totais": {"gastos": total_gastos, "hotel_2_noites": round(hotel_eur, 2), "hotel_no_dia": round(hotel_dia, 2), "total": round(total, 2), "por_pessoa": round(pp, 2), "por_pessoa_brl": round(pp * COTACAO, 2), **{k: round(v, 2) for k, v in cat.items()}}},
              open("rev1/linha_do_tempo_rev1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(ms):
        return f"{int(ms // 60000):02d}:{(ms % 60000) / 1000:04.1f}"

    linhas = ["# REV1 · Efeitos visuais e sonoros (vlog de Bruxelas)", "",
              "Gerado por `rev1/montar_rev1.py`. Minutos no **vídeo final** (gancho + corpo decupado + fechamento). Cores dos efeitos: camada de efeitos (decisão do Diego, 21/10/2026, no vlog de Amsterdam); objetos da marca nas cores do DS.", "",
              "| Entra | Dura | Efeito | Por quê |", "|---|---:|---|---|"]
    for e in sorted(efeitos, key=lambda x: x["ms"]):
        d = f"{e['dur'] / 1000:.1f} s" if e["dur"] else ""
        linhas.append(f"| {mmss(e['ms'])} | {d} | {e['nome']} | {e['porque']} |")
    open("rev1/efeitos_rev1.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")

    def seg(ms):
        return f"{ms / 1000:.2f}".replace(".", ",") + " s"

    lt = ["# REV1 · Takes do gancho e do fechamento (vlog de Bruxelas)", "",
          f"Cada take com pelo menos {MIN_TAKE:.0f} s e sem corte de cena dentro (conferido contra `CENAS`). Tempos no vídeo final; a fonte é `fonte/1103_fala.mp4` (minutos da fonte entre parênteses).", "",
          "| Bloco | Entra | Dura | Fonte | Plano |", "|---|---|---:|---|---|"]
    for bloco, ini, dur, c in takes:
        lt.append(f"| {bloco} | {mmss(ini)} | {seg(dur)} | {mmss(c['de'] * 1000)}–{mmss(c['ate'] * 1000)} | {c['o_que']} |")
    menor = min(d for _, _, d, _ in takes) / 1000
    lt += ["", f"Menor take: **{seg(menor * 1000)}**.", "", "## Narrações a gravar (tempo previsto)", "", "| Bloco | No vídeo | Texto |", "|---|---|---|"]
    for n in narr:
        lt.append(f"| {n['id']} | {mmss(n['fala_ini'])}–{mmss(n['fala_fim'])} ({(n['fala_fim'] - n['fala_ini']) / 1000:.1f} s) | {n['texto']} |")
    open("rev1/takes_rev1.md", "w", encoding="utf-8").write("\n".join(lt) + "\n")

    print(f"gancho {G / 1000:.2f} s · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} ({(F_fim - B_fim) / 1000:.1f} s) · total {mmss(duracao)}")
    print(f"trechos {len(trechos)} · eventos {len(ev)} · menor take {menor:.2f} s · hotel {mmss(h0)}")
    print(f"gastos {eur(total_gastos)} · hotel 2 noites {eur(hotel_eur)} ({brl(HOTEL_BRL)}) · no dia {eur(hotel_dia)} · total {eur(total)} · por pessoa {eur(pp)} ({brl(pp * COTACAO)}) · {cat}")
    for n in narr:
        print(f"  {n['id']} {mmss(n['fala_ini'])} {n['texto']}")


if __name__ == "__main__":
    sys.exit(main())
