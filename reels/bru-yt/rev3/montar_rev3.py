"""Montagem da REV3 do vlog de Bruxelas (vídeo longo do YouTube, 16:9, 30 fps). Parte da REV2 (`rev2/montar_rev2.py`,
não alterada) e acrescenta o pedido do Diego de 06/11/2026: "quando o primeiro dia aparece, tem que aparecer a data
no canto superior esquerdo: 15 de Março de 2026", "nas cores do placar, um pouco menor que essa placa" (painel do
Placar, x 96 · y 72).

O que a REV2 já fazia (partindo da REV1):

  - narrações gravadas (fonte/narracao/N01–N12, "Praça Ernesto Lebram" no Drive), encaixadas pelo que foi DITO
    (Whisper large-v3): gancho N10 · N11 · N12, hotel N01, fechamento N02 · N03 · N06 · N07 · N08 · N09 (N04 diz
    "120 reais"; N05 para no total: ficaram de fora);
  - gancho e fechamento com os mesmos planos aprovados, esticados ou com planos do mesmo tipo para caber a fala;
  - decupagem sem pedaços < 0,7 s e sem os quadros de câmera virando da gravação (`rev3/edl_rev3.json`), com a imagem
    congelada onde a fala já começou;
  - print real do hotel (o preço de uma busca nova, R$ 655/R$ 769 de 8 a 9/11, foi coberto);
  - bilhete do metrô: 10 viagens, € 18 por pessoa (Diego); a tarifa oficial do Brupass 10 em 2026 é € 18,90;
  - Bilhete do veredito com o veredito novo ("vale, mas 1 dia basta").

Escreve (de reels/bru-yt):  python rev3/montar_rev3.py
  rev3/props_rev3.json, rev3/linha_do_tempo_rev3.json, rev3/efeitos_rev3.md, rev3/takes_rev3.md

Valores: registro do Diego (06/11/2026). Real ↔ euro pela PTAX de venda de 13/03/2026: € 1 = R$ 6,0128.
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
NOITES_NO_DIA = 1  # o total de Bruxelas leva 1 das 2 noites; a outra é do bate-volta a Bruges (Diego, 06/11/2026)
BILHETE_EUR = 18.00  # bilhete de 10 viagens, € 18 por pessoa (Diego, 06/11/2026); Brupass 10 oficial: € 18,90 desde 01/02/2026


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


# cortes de cena da fonte (ffmpeg scene > 0,22; _tmp/cenas.json), só os que cercam os takes. REV3: sem as rajadas
# de 296,57 e 304,50 (são panorâmicas, conferidas quadro a quadro); o corte real das fachadas para a torre é 298,87
CENAS = [27.07, 29.73, 33.07, 36.57, 43.70, 46.33, 108.33, 111.43, 115.23, 119.07, 132.37, 140.67, 167.77, 181.00, 183.70,
         203.00, 208.03, 212.30, 215.23, 217.93, 222.37, 226.27, 290.80, 294.17, 298.87, 302.00, 307.50, 325.73,
         328.47, 331.37, 334.37, 421.20, 426.40, 429.83, 433.10, 447.07, 463.03, 528.17, 531.10, 534.00, 537.93, 540.00, 543.17,
         546.50, 550.10, 554.77, 557.43, 608.87, 618.53, 623.40, 627.00, 673.90, 676.37, 678.47, 680.83, 684.33, 787.17, 790.33,
         796.30, 798.37, 802.57, 862.23]

# ------------------------------------------------------------------------------------------------
# GANCHO (fonte em s). Os mesmos planos da REV1 (aprovados pelo Diego), esticados para a narração gravada, que ficou
# mais longa que o roteiro. `sons`: pedaços de som do take quando não é o da própria imagem (s do take, fonte, tipo).
GANCHO = [
    {"de": 108.40, "ate": 111.40, "o_que": "Atomium de baixo para cima, céu azul (12h19)", "som": "baixo"},
    {"de": 294.25, "ate": 296.65, "o_que": "fachada da Grand Place (para caber a G1; o Atomium de longe fica só no fechamento)", "som": "baixo"},
    {"de": 134.75, "ate": 139.45, "o_que": "Zinneke: \"Ponto turístico de Bruxelas… Um cachorro mijando.\"", "som": "fala"},
    {"de": 181.05, "ate": 183.05, "o_que": "batata e sanduíche da Fritland (close), na \"batata frita\" da G2", "som": "baixo"},
    {"de": 331.40, "ate": 333.40, "o_que": "waffle com Nutella (close), no \"waffle, chocolate\" da G2", "som": "baixo"},
    {"de": 426.42, "ate": 429.77, "o_que": "vitrine dos ovos de Páscoa, no \"não teve nem coragem de chegar perto\"; no fim, o som de \"seis ovos de páscoa…\"", "som": "fala",
     "sons": [(0.0, 2.10, 426.42, "gancho_baixo"), (2.10, 3.35, 447.10, "gancho_fala")]},
    {"de": 448.35, "ate": 453.15, "o_que": "Diego: \"…menores que meu dedo, estão a 26 euros pela vitrine.\"", "som": "fala"},
    # REV3: termina em 456,79 (silêncio): até 457,00 entrava o começo do "Vamos" (456,92, medido pela energia); a
    # mesma duração da REV2 (62 quadros), começando 0,22 s antes, no burburinho da galeria
    {"de": 454.72, "ate": 456.79, "o_que": "Diego: \"Não tem condições.\"", "som": "fala"},
    {"de": 217.94, "ate": 222.34, "o_que": "chegada na Grand Place (dia)", "som": "baixo"},
    {"de": 528.25, "ate": 531.05, "o_que": "Manneken Pis vestido de jogador de futebol (para caber a G3)", "som": "baixo"},
    {"de": 862.25, "ate": 867.25, "o_que": "Grand Place à noite, no \"esse é o nosso primeiro dia em Bruxelas\"", "som": "baixo"},
]
# narrações gravadas (fonte/narracao/): onde a FALA começa no relógio do bloco (ms), a fala no arquivo (s, por energia)
# e o texto como foi dito (Whisper large-v3, a conferir na escuta)
NARRACAO_GANCHO = [
    {"id": "G1", "arq": "N10", "em": 250, "fala": (0.63, 5.14), "texto": "Será que vale a pena passar um dia inteiro em Bruxelas? E quanto será que custa isso?"},
    {"id": "G2", "arq": "N11", "em": None, "ancora": ("fries", 0.10), "fala": (0.54, 6.27), "texto": "Bom, teve batata frita, waffle, chocolate e alguns que a gente não teve nem coragem de chegar perto."},
    {"id": "G3", "arq": "N12", "em": None, "ancora": ("gp", 0.20), "fala": (0.71, 11.86), "texto": "Eu anotei cada euro que a gente gastou nesse nosso rolê em Bruxelas. No final do vídeo você vai ver quanto custou tudo e se realmente vale a pena. Então fique com a gente, porque esse é o nosso primeiro dia em Bruxelas."},
]

# HOTEL (pedido do Diego: no 4:50 da fonte, sobre a montagem das fachadas, antes da fala da Jeanneke Pis)
NARRACAO_HOTEL = {"id": "H1", "arq": "N01", "src": 290.30, "fala": (2.00, 21.13),
                  "texto": "E falando em hotel, a gente ficou no ibis Brussels off Grand Place, a uns 200 metros da praça. Juro, era colado, parecia que eu tava dentro dela já. Esse foi o mais barato que encontramos próximo do centro. Como a gente ia ficar só um dia aqui, preferimos ficar perto de tudo. Ficamos duas noites, uma pra Bruxelas e uma pro bate e volta de Bruges. No total, isso tudo deu 1.738 para o casal."}

# FECHAMENTO: os planos da REV1 + 3 do mesmo tipo (a narração gravada tem 49,6 s de fala, contra 38,5 s do roteiro)
FECHAMENTO = [
    {"de": 862.25, "ate": 867.25, "o_que": "Grand Place à noite (os \"cortes finais\" do Diego, 14:22)"},
    {"de": 790.34, "ate": 796.26, "o_que": "Boulevard Anspach na hora azul"},
    {"de": 208.05, "ate": 212.25, "o_que": "guarda-sóis da Fritland (F2: comida)"},
    {"de": 678.50, "ate": 680.80, "o_que": "vitrine do Aux Merveilleux de Fred (F2: doce)"},
    {"de": 290.82, "ate": 294.12, "o_que": "fachadas douradas da Grand Place (F3: hotel colado na praça)"},
    {"de": 298.90, "ate": 301.98, "o_que": "torre da Prefeitura na Grand Place (REV3: começa depois do corte real de 298,87; na REV1 piscavam 4 quadros da fachada)"},
    {"de": 787.20, "ate": 790.30, "o_que": "terraços do Boulevard Anspach no fim da tarde"},
    {"de": 618.60, "ate": 623.35, "o_que": "jardim do Mont des Arts no fim da tarde (F4: o charme)"},
    {"de": 623.45, "ate": 626.95, "o_que": "Mont des Arts com o sol baixo"},
    {"de": 540.05, "ate": 543.10, "o_que": "jardim do Mont des Arts de dia"},
    {"de": 550.15, "ate": 554.70, "o_que": "Praça Real (Saint-Jacques-sur-Coudenberg)"},
    {"de": 421.20, "ate": 426.36, "o_que": "Galerias Reais Saint-Hubert (F5)"},
    {"de": 111.50, "ate": 115.20, "o_que": "Atomium de longe"},
    {"de": 215.28, "ate": 217.90, "o_que": "Bolsa de Bruxelas (F6), vira a página para a tela final"},
]
NARRACAO_FECHAMENTO = [
    # REV3 (Diego, 06/11/2026): sai "que era do lado" (soava como se o Atomium fosse vizinho da Grand Place); o corte
    # vai de silêncio a silêncio (energia medida) e o "e" fica
    {"id": "F1", "arq": "N02", "fala": (1.33, 9.43), "cortes": [(6.09, 6.765)], "texto": "E um dia só, a gente bateu perna por Bruxelas inteira. Nós fomos do Atomium até a Grand Place, e passamos pelas três estátuas fazendo xixi."},
    {"id": "F2", "arq": "N03", "fala": (0.60, 5.09), "texto": "Metrô, comida, cerveja e doce. O dia para o casal deu 94 euros."},
    {"id": "F3", "arq": "N06", "fala": (1.05, 9.88), "texto": "E somando uma noite de hotel referente a esse dia que a gente passou aqui hoje, ficou uns 239 euros pro casal, 119 pra cada, que isso dá mais ou menos 720 reais."},
    {"id": "F4", "arq": "N07", "fala": (0.95, 16.13), "texto": "Mas e aí, vale a pena? Bom, eu diria que sim, mas não mais que um dia. Esse dia foi suficiente pra gente conhecer o charme, os doces e a cerveja de Bruxelas. Se eu tivesse a oportunidade de fazer diferente, eu me hospedaria numa cidade próxima, como Paris ou até mesmo Bruges, na Bélgica, e viria pra cá de bate e volta."},
    {"id": "F5", "arq": "N08", "fala": (0.78, 8.79), "texto": "Se esse vídeo te ajudou de alguma forma e puder se inscrever ou deixar o like aqui, vai ser muito importante para mim. Também não esquece de me seguir no Instagram, arroba primeirodiaem."},
    {"id": "F6", "arq": "N09", "fala": (0.80, 4.27), "texto": "Toda cidade tem um primeiro dia, e o próximo é em Bruges. A gente se vê lá!"},
]
def dur_narr(n):
    """Duração da fala da narração (s), descontados os cortes internos."""
    return (n["fala"][1] - n["fala"][0]) - sum(b - a for a, b in n.get("cortes", []))


def t_narr(n, t):
    """Tempo `t` do arquivo (s) → tempo dentro da fala já cortada (s)."""
    return (t - n["fala"][0]) - sum(b - a for a, b in n.get("cortes", []) if b <= t)


FECH_INICIO = 1200  # a Grand Place à noite abre com a música; a F1 entra 1,2 s depois
FECH_INTERVALO = 500  # entre o fim de uma narração e o começo da seguinte
FECH_RESPIRO = 2400  # depois da F6, antes de a página virar


def palavra_narr(tr_n, arq, alvo, depois=0.0):
    """Tempo (s, no arquivo) da palavra `alvo` na transcrição da narração."""
    for w in tr_n[arq]:
        if w["ini"] >= depois and w["p"].lower().strip(".,!?") == alvo:
            return w["ini"]
    raise SystemExit(f"{arq}: palavra {alvo!r} não achada")


# GASTOS (fonte em s; valores do Diego, 06/11/2026). hora = relógio do clipe na tela (hora do arquivo no acervo).
GASTOS = [
    {"t": 33.10, "lugar": "METRÔ · STIB", "hora": "12:15", "linhas": [("Bilhete de 10 viagens × 2", 2 * BILHETE_EUR)], "cat": "transporte",
     "porque": "Diego: 00:33, 18 euros por pessoa (confirmado em 06/11); \"a gente pegou um de 10 viagens\". A tarifa oficial do Brupass 10 em 2026 é € 18,90 (SNCB/STIB): ficou o valor do registro. Entra no 1º plano depois do metrô (saída no Heysel, 12h15)"},
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
    edl = json.load(open("rev3/edl_rev3.json", encoding="utf-8"))
    tr_n = json.load(open("_tmp/narr/transcricao_narracoes.json", encoding="utf-8"))
    confere_takes(GANCHO, "gancho")
    confere_takes(FECHAMENTO, "fechamento")
    q = lambda ms: round(ms * FPS / 1000)  # noqa: E731
    trechos, audio, efeitos, takes = [], [], [], []

    def ef(ms, nome, porque, dur=None):
        efeitos.append({"ms": ms, "nome": nome, "porque": porque, "dur": dur})

    # ---------- gancho ----------
    pos = 0
    inicio_take = {}
    for c in GANCHO:
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        trechos.append({"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur})
        if "sons" in c:
            for t0, t1, src, tipo in c["sons"]:
                audio.append({"src": src, "out": pos + t0 * 1000, "dur": (min(t1 * 1000, dur) - t0 * 1000), "tipo": tipo})
        else:
            audio.append({"src": c["de"], "out": pos, "dur": dur, "tipo": "gancho_" + c["som"]})
        takes.append(("gancho", pos, dur, c))
        inicio_take[c["de"]] = pos
        pos += dur
    G = pos
    ancora = {"fries": inicio_take[181.05], "gp": inicio_take[217.94]}
    for n in NARRACAO_GANCHO:
        if n["em"] is None:
            k, folga = n["ancora"]
            n["em"] = ancora[k] + folga * 1000

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
    # quadros congelados (câmera virando com a fala já começando): a imagem para num quadro bom e o som segue
    for cg in edl.get("congelar", []):
        a0, a1 = mp.ms(cg["de"]), mp.ms(cg["ate"])
        novos = []
        for tr_ in trechos:
            if tr_["de"] < a1 and tr_["ate"] > a0 and "congela" not in tr_:
                if tr_["de"] < a0:
                    novos.append({**tr_, "ate": a0})
                novos.append({"src": round(cg["quadro"] * 1000), "de": max(a0, tr_["de"]), "ate": min(a1, tr_["ate"]), "congela": True})
                if tr_["ate"] > a1:
                    novos.append({**tr_, "src": tr_["src"] + round(a1 - tr_["de"]), "de": a1})
            else:
                novos.append(tr_)
        trechos = novos
        ef(a0, f"Quadro congelado ({(a1 - a0) / 1000:.2f} s)", cg["motivo"], a1 - a0)

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
    # data (pedido do Diego, 06/11/2026: "quando o primeiro dia aparece, tem que aparecer a data no canto superior
    # esquerdo"; depois: "nas cores do placar, um pouco menor que essa placa"): painel do Placar (grafite, amarelo,
    # 56 px, 96 px de altura) na posição do Placar no 16:9 (x 96 · y 72), junto com a placa da marca. Sem som
    ev.append({"tipo": "data", "texto": "15 de março de 2026", "ini": G + 700, "fim": G + 4400})
    ef(G + 700, "Data \"15 DE MARÇO DE 2026\" no painel do Placar (canto superior esquerdo, sem som)", "Pedido do Diego (06/11/2026): a data quando o primeiro dia aparece, nas cores do Placar e menor que a placa. Material, fonte, altura e acender do Placar (DS 2.5), na posição dele (x 96 · y 72); o 1º Placar de gasto só entra em 1:06", 3700)
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
    nh = NARRACAO_HOTEL
    h0 = mp.ms(nh["src"])
    h_dur = (nh["fala"][1] - nh["fala"][0]) * 1000
    hotel_eur = HOTEL_BRL / COTACAO
    em_h = lambda pal, depois=0.0: h0 + (palavra_narr(tr_n, nh["arq"], pal, depois) - nh["fala"][0]) * 1000  # noqa: E731
    t_print = em_h("ibis") - 300
    t_rh = em_h("ficamos") - 200
    fim_print = t_rh - 250
    ev.append({"tipo": "print", "arquivo": "print_hotel.png", "endereco": "ibis Brussels off Grand Place · página do hotel", "ini": t_print, "fim": fim_print, "x": 800, "y": 100, "largura": 1040, "alturaJanela": 640, "rolagem": 0})
    ef(t_print, "Print da página do hotel (janela de navegador): fachada, bar, terraço e salão", "Print do Diego (06/11/2026). O preço de uma busca nova (R$ 655 / R$ 769, 8–9/11) foi coberto: não é o da viagem. Entra no \"ibis\" e sai antes do Recibo", fim_print - t_print)
    ev.append({"tipo": "recibo", "lugar": "IBIS OFF GRAND PLACE", "cabecalho": "HOSPEDAGEM · 2 NOITES · 2 PESSOAS", "linhas": [["2 noites", brl(HOTEL_BRL)], ["por noite", brl(HOTEL_BRL / 2)]],
               "total": eur(hotel_eur), "real": f"pago {brl(HOTEL_BRL)}", "rodape": RODAPE, "ini": t_rh, "fim": h0 + h_dur + 700, "x": 1400, "y": 150, "escala": 0.72})
    ef(t_rh, f"Recibo da hospedagem: {brl(HOTEL_BRL)} = {eur(hotel_eur)} (2 noites)", "No \"Ficamos duas noites\" (H1). R$ 1.738,78 para duas pessoas e duas noites; fora do Placar do dia (regra de Amsterdam); 1 noite entra no total do fechamento", h0 + h_dur + 700 - t_rh)

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

    # ---------- fechamento: narrações em sequência e objetos nas palavras ----------
    f = B_fim
    pos_n = FECH_INICIO
    fech = {}
    for n in NARRACAO_FECHAMENTO:
        n["em"] = pos_n
        fech[n["id"]] = n
        pos_n += dur_narr(n) * 1000 + FECH_INTERVALO
    fim_falas = pos_n - FECH_INTERVALO
    assert f + fim_falas + FECH_RESPIRO <= F_fim + 1, f"faltam {(f + fim_falas + FECH_RESPIRO - F_fim) / 1000:.2f} s de imagem no fechamento"

    def em_f(bid, pal, depois=0.0):
        n = fech[bid]
        return f + n["em"] + t_narr(n, palavra_narr(tr_n, n["arq"], pal, depois)) * 1000

    def fim_f(bid):
        n = fech[bid]
        return f + n["em"] + dur_narr(n) * 1000

    noite = hotel_eur / 2
    hotel_dia = noite * NOITES_NO_DIA
    total = total_gastos + hotel_dia
    pp = total / 2
    cat = {"comida": 0.0, "transporte": 0.0}
    for g in GASTOS:
        cat[g.get("cat", "comida")] += valor(g)
    assert abs(sum(cat.values()) - total_gastos) < 0.005
    t_mapa = em_f("F1", "nós") - 2600
    ev.append({"tipo": "mapa", "arquivo": "mapa_dia_centro.json", "ini": t_mapa, "fim": fim_f("F1") + 600, "desenho": 4200})
    ef(t_mapa, "Mapa do dia no centro (9 paradas, da Zinneke ao Spago)", "F1 (\"a gente bateu perna por Bruxelas inteira… passamos pelas três estátuas\"): o roteiro a pé. Entra depois de alguns segundos da Grand Place à noite", fim_f("F1") + 600 - t_mapa)
    t_rec = em_f("F2", "metrô") - 200
    t_hot = em_f("F3", "somando") - 100
    fim_rec = fim_f("F3") + 900
    ev.append({"tipo": "recibo", "lugar": "1 DIA EM BRUXELAS", "cabecalho": "DOM 15/03 · 2 PESSOAS · SEM PASSAGEM", "linhas": [["Comida e bebida", eur(cat["comida"])], ["Metrô", eur(cat["transporte"])], ["Hotel (1 noite)", eur(hotel_dia)]],
               "total": eur(total), "real": f"{eur(pp)} por pessoa ≈ {brl(pp * COTACAO)}", "rodape": RODAPE, "ini": t_rec, "fim": fim_rec, "x": 1360, "y": 96, "escala": 0.78,
               "aparecer": [0, 0, round(t_hot - t_rec)], "totais": [{"total": eur(total_gastos), "real": f"{eur(total_gastos / 2)} por pessoa"}, {"total": eur(total_gastos), "real": f"{eur(total_gastos / 2)} por pessoa"}, {"total": eur(total), "real": f"{eur(pp)} por pessoa ≈ {brl(pp * COTACAO)}"}]})
    ef(t_rec, f"Recibo do dia: {eur(total_gastos)} sem hotel → {eur(total)} com 1 noite ({eur(pp)} por pessoa)", "Entra no \"Metrô, comida, cerveja e doce\" (F2); a linha do hotel e o total novo entram no \"somando uma noite de hotel\" (F3). Responde à pergunta do gancho", fim_rec - t_rec)
    t_bil = em_f("F4", "sim") - 100
    ev.append({"tipo": "bilhete", "texto": "vale! mas|1 dia basta", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": t_bil, "saida": em_f("F4", "esse") + 2400})
    ef(t_bil, "Bilhete do veredito: \"vale! mas 1 dia basta\" + ✓", "No \"eu diria que sim, mas não mais que um dia\" (F4). A REV1 dizia \"vale muito! leve luva\"; o veredito gravado mudou", em_f("F4", "esse") + 2400 - t_bil)
    t_like = em_f("F5", "inscrever") - 400
    ev.append({"tipo": "like", "entrada": t_like, "saida": t_like + 3300})
    ef(t_like, "Animação \"DEIXA O LIKE E SE INSCREVE\" (2ª vez)", "No \"puder se inscrever ou deixar o like aqui\" (F5)", 3540)
    t_ig = em_f("F5", "instagram") - 500
    ev.append({"tipo": "instagram", "ini": t_ig, "fim": fim_f("F5") + 700})
    ef(t_ig, "Chamada SEGUE NO INSTAGRAM (3ª vez)", "No \"me seguir no Instagram, arroba primeirodiaem\" (F5)", fim_f("F5") + 700 - t_ig)
    t_placa = f + fech["F6"]["em"]
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": t_placa, "saida": F_fim - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": t_placa + 400, "relDb": -12})
    ef(t_placa, "Placa de fechamento \"TODA CIDADE TEM UM PRIMEIRO DIA.\" + Nascer do 1º", "No \"Toda cidade tem um primeiro dia\" (F6)", F_fim - t_placa)
    ev.append({"tipo": "telafinal", "ini": F_fim, "proximo": "bruges"})
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: bruges →\")", "Doc., seção 2. Ordem dos vlogs (CLAUDE.md, pendência 11): Amsterdam, Bruxelas, Bruges…", TELA_FINAL)

    # narrações no relógio do vídeo final: arquivo, onde a fala começa e termina, trecho de fala no arquivo
    narr = []
    for base, lista in [(0, NARRACAO_GANCHO), (B_fim, NARRACAO_FECHAMENTO)]:
        for n in lista:
            f0, f1 = n["fala"]
            narr.append({"id": n["id"], "arq": f"narracao/{n['arq']}.m4a", "fala_ini": base + n["em"], "fala_fim": base + n["em"] + dur_narr(n) * 1000, "arq_ini_s": f0, "arq_fim_s": f1, "cortes": n.get("cortes", []), "texto": n["texto"]})
    narr.append({"id": "H1", "arq": f"narracao/{nh['arq']}.m4a", "fala_ini": h0, "fala_fim": h0 + h_dur, "arq_ini_s": nh["fala"][0], "arq_fim_s": nh["fala"][1], "texto": nh["texto"]})
    narr.sort(key=lambda n: n["fala_ini"])
    for a_, b_ in zip(narr, narr[1:]):
        assert a_["fala_fim"] + 150 <= b_["fala_ini"], (a_["id"], b_["id"])
    assert narr[2]["fala_fim"] <= G - 300, "a G3 passa do gancho"
    assert mp.ms(311.22) >= h0 + h_dur + 200, f"a narração do hotel passa da fala da Jeanneke ({(h0 + h_dur - mp.ms(311.22)) / 1000:.2f} s)"
    assert narr[-1]["fala_fim"] < F_fim - 300

    if a.guia:
        frases = [{"ini": n["fala_ini"], "fim": n["fala_fim"], "texto": f"{n['id']} · {n['texto']}"} for n in narr]
        ev.append({"tipo": "guia", "inicio": 0, "fim": G, "frases": frases})
        ev.append({"tipo": "guia", "inicio": h0 - 1500, "fim": h0 + h_dur + 1500, "frases": frases})
        ev.append({"tipo": "guia", "inicio": B_fim, "fim": F_fim, "topo": True, "frases": frases})

    props = {"video": "http://127.0.0.1:8787/proxy1080.mp4", "duracao": duracao, "fps": FPS, "trechos": trechos, "eventos": ev, "zooms": zooms, "refLufs": REF}
    sufixo = "_guia" if a.guia else ""
    json.dump(props, open(f"rev3/props_rev3{sufixo}.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"fps": FPS, "gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio, "narracoes": narr,
               "hotel_ms": [h0, h0 + h_dur], "manter": manter,
               "totais": {"gastos": total_gastos, "hotel_2_noites": round(hotel_eur, 2), "hotel_no_dia": round(hotel_dia, 2), "total": round(total, 2), "por_pessoa": round(pp, 2), "por_pessoa_brl": round(pp * COTACAO, 2), **{k: round(v, 2) for k, v in cat.items()}}},
              open("rev3/linha_do_tempo_rev3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(ms):
        d = int(round(ms / 100))  # décimos (evita "14:60.0")
        return f"{d // 600:02d}:{(d % 600) / 10:04.1f}"

    linhas = ["# REV3 · Efeitos visuais e sonoros (vlog de Bruxelas)", "",
              "Gerado por `rev3/montar_rev3.py`. Minutos no **vídeo final** (gancho + corpo decupado + fechamento). Cores dos efeitos: camada de efeitos (decisão do Diego, 21/10/2026, no vlog de Amsterdam); objetos da marca nas cores do DS.", "",
              "| Entra | Dura | Efeito | Por quê |", "|---|---:|---|---|"]
    for e in sorted(efeitos, key=lambda x: x["ms"]):
        d = f"{e['dur'] / 1000:.1f} s" if e["dur"] else ""
        linhas.append(f"| {mmss(e['ms'])} | {d} | {e['nome']} | {e['porque']} |")
    open("rev3/efeitos_rev3.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")

    def seg(ms):
        return f"{ms / 1000:.2f}".replace(".", ",") + " s"

    lt = ["# REV3 · Takes do gancho e do fechamento (vlog de Bruxelas)", "",
          f"Cada take com pelo menos {MIN_TAKE:.0f} s e sem corte de cena dentro (conferido contra `CENAS`). Tempos no vídeo final; a fonte é `fonte/1103_fala.mp4` (minutos da fonte entre parênteses).", "",
          "| Bloco | Entra | Dura | Fonte | Plano |", "|---|---|---:|---|---|"]
    for bloco, ini, dur, c in takes:
        lt.append(f"| {bloco} | {mmss(ini)} | {seg(dur)} | {mmss(c['de'] * 1000)}–{mmss(c['ate'] * 1000)} | {c['o_que']} |")
    menor = min(d for _, _, d, _ in takes) / 1000
    lt += ["", f"Menor take: **{seg(menor * 1000)}**.", "", "## Narrações (como foram ditas; transcrição automática, a confirmar na escuta)", "", "| Bloco | Arquivo | No vídeo | Texto |", "|---|---|---|---|"]
    for n in narr:
        lt.append(f"| {n['id']} | `{n['arq']}` | {mmss(n['fala_ini'])}–{mmss(n['fala_fim'])} ({(n['fala_fim'] - n['fala_ini']) / 1000:.1f} s) | {n['texto']} |")
    open("rev3/takes_rev3.md", "w", encoding="utf-8").write("\n".join(lt) + "\n")

    print(f"gancho {G / 1000:.2f} s · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} ({(F_fim - B_fim) / 1000:.1f} s) · total {mmss(duracao)}")
    print(f"trechos {len(trechos)} · eventos {len(ev)} · menor take {menor:.2f} s · hotel {mmss(h0)}")
    print(f"gastos {eur(total_gastos)} · hotel 2 noites {eur(hotel_eur)} ({brl(HOTEL_BRL)}) · no dia {eur(hotel_dia)} · total {eur(total)} · por pessoa {eur(pp)} ({brl(pp * COTACAO)}) · {cat}")
    for n in narr:
        print(f"  {n['id']} {mmss(n['fala_ini'])} {n['texto']}")


if __name__ == "__main__":
    sys.exit(main())
