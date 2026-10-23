"""Montagem da REV3 do vlog de Amsterdam (vídeo longo do YouTube, 16:9). Parte da REV2 (`rev2/montar_rev2.py`; a
decupagem do corpo continua a da REV1, `rev1/edl_rev1.json`) e aplica os pedidos do Diego de 23/10/2026 (noite):

  - o fechamento inteiro regravado (F1 a F7, `fonte/narracao/fechamento_v2/`), com texto novo; os planos do
    fechamento foram remontados para o tempo novo (cada take continua com pelo menos 2 s);
  - Placar com o HORÁRIO real de Amsterdam no momento da gravação (hora do arquivo), não mais o cronômetro "+HH:MM";
  - Placar só aparece quando um gasto é somado: liga logo antes do Recibo, soma, fica 3 s e apaga;
  - o 1º gasto (ônibus 397) entra na cena de dentro do ônibus (IMG_1377, 14:38), e não durante a fala no aeroporto;
  - O'Donnell's com horário estimado de 14:45: na edição do Diego ele vem depois da fachada da Heineken (14:37);
  - print do Hoteis.com mais curto, saindo antes do Diego virar a câmera para mostrar o quarto.
O resto (gancho, corpo, confete, rufar, recibos, músicas) é o da REV2.

Escreve (de reels/ams-yt):  python rev3/montar_rev3.py [--guia]
  rev3/props_rev3.json            props da composição `VideoLongo` (Remotion)
  rev3/linha_do_tempo_rev3.json   trechos de áudio para a mixagem (fonte → saída), narrações e músicas
  rev3/efeitos_rev3.md            relatório de cada efeito: minuto em que entra e por quê
  rev3/takes_rev3.md              os takes do gancho e do fechamento, com a duração de cada um

Valores: registro do Diego (21 e 23/10/2026); o real é convertido pela PTAX de venda de 12/03/2026 (Banco Central),
€ 1 = R$ 5,9978. O ônibus 397 não está no registro: vale a tarifa oficial (Transdev/Connexxion, € 6,50 a viagem).
"""
import argparse
import json
import sys
from bisect import bisect_right
from decimal import ROUND_HALF_UP, Decimal

FPS = 24
COTACAO = 5.9978
RODAPE = "cotação € 1 = R$ 5,9978 · PTAX 12/03/2026"
TELA_FINAL = 20000
DUR_PAGINA = 700
MIN_TAKE = 2.0  # pedido do Diego (23/10/2026): nenhum take do gancho ou do fechamento abaixo de 2 s


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


# ------------------------------------------------------------------------------------------------
# Cortes de cena da fonte em volta dos takes (detectados no export de 1080p, limiar 0,25), para provar que nenhum
# take tem corte interno: cada take começa e termina dentro de um único plano.
CENAS = [124.17, 128.17, 129.71, 134.88, 139.12, 293.67, 298.21, 303.12, 594.04, 845.92, 857.42, 1174.54, 1178.04,
         1245.12, 1247.96, 1309.96, 1312.67, 1315.58, 1348.62, 1351.00, 1354.33, 1356.42, 1359.62, 1642.33, 1645.62, 1648.88,
         1912.67, 1918.67, 1922.54]

# GANCHO (fonte em s). Narração gravada pelo Diego (22/10/2026), tomadas G_1, G_3 e G_4 (a G_2 é uma tomada
# mais curta da G_3). Falas reais: Marina ("Gente, meu cabelo!") e Diego ("Bebi quatro, estou realizado.").
GANCHO = [
    {"de": 135.15, "ate": 138.15, "o_que": "canal com as casas tortas (Damrak, dia 1)", "som": "baixo"},
    {"de": 211.90, "ate": 214.10, "o_que": "vento no cabelo: \"Gente, meu cabelo!\"", "som": "fala"},
    {"de": 846.90, "ate": 849.05, "o_que": "chuva, guarda-chuva do hotel (dia 2)", "som": "baixo"},
    {"de": 1646.20, "ate": 1648.25, "o_que": "bicicletas em De Pijp (dia 3)", "som": "baixo"},
    {"de": 1159.60, "ate": 1161.65, "o_que": "stroopwafel do Rudi's (dia 2)", "som": "baixo"},
    {"de": 1865.30, "ate": 1867.70, "o_que": "Heineken: \"Bebi quatro, estou realizado.\"", "som": "fala"},
    {"de": 48.00, "ate": 51.15, "o_que": "quarto do XO Hotel Inner (dia 1)", "som": "baixo"},
    {"de": 1915.30, "ate": 1918.60, "o_que": "canais à noite (dia 3)", "som": "baixo"},
]
# narrações: arquivo (fonte/narracao/...), onde a FALA começa (ms no relógio do bloco), fala no arquivo (s, por
# energia: o início do arquivo tem um clique do gravador) e o texto como foi dito (Whisper large-v3, a conferir)
NARRACAO_GANCHO = [
    {"arq": "inicio/G_1.m4a", "em": 250, "fala": (0.51, 2.74), "texto": "Quanto custou três dias em Amsterdã?"},
    {"arq": "inicio/G_3.m4a", "em": 5750, "fala": (0.57, 6.00), "texto": "Teve muito frio, chuva, bicicleta pra todo lado, além de muito stroopwafel e cerveja, é claro, né?"},
    {"arq": "inicio/G_4.m4a", "em": 14050, "fala": (0.31, 6.13), "texto": "E tem um detalhe na conta: o hotel custou mais do que todo o resto. Então pega sua pipoca e fica até o final, que eu vou lhe mostrar."},
]

# FECHAMENTO: clipes sem fala depois do último plano do Diego (o dia vira pôr do sol e noite). REV3: remontado para o
# texto novo (F2 fala de canais, pontes e bicicletas; o "vale muito a pena" está no fim do F5)
FECHAMENTO = [
    {"de": 124.30, "ate": 127.80, "o_que": "casas na beira do canal (dia 1)"},
    {"de": 129.80, "ate": 132.40, "o_que": "canal com a bicicleta na grade (dia 1)"},
    {"de": 1356.50, "ate": 1359.50, "o_que": "ponte com flores e bicicleta vermelha (dia 2)"},
    {"de": 1642.40, "ate": 1645.50, "o_que": "rua de De Pijp com ciclistas passando (dia 3)"},
    {"de": 294.25, "ate": 298.15, "o_que": "Palácio Real na Praça Dam (dia 1)"},
    {"de": 594.20, "ate": 597.50, "o_que": "Munttoren no fim da tarde (dia 1)"},
    {"de": 1175.00, "ate": 1177.90, "o_que": "Rijksmuseum (dia 2)"},
    {"de": 1312.75, "ate": 1315.50, "o_que": "barco no canal (dia 2)"},
    {"de": 1348.68, "ate": 1350.98, "o_que": "Herengracht (dia 2)"},
    {"de": 1351.05, "ate": 1354.30, "o_que": "canal com árvores (dia 2)"},
    {"de": 1245.20, "ate": 1247.40, "o_que": "chafariz do Vondelpark (dia 2)"},
    {"de": 852.20, "ate": 855.10, "o_que": "os dois rindo debaixo do guarda-chuva (dia 2)"},
    {"de": 1903.90, "ate": 1910.65, "o_que": "pôr do sol nos canais (dia 3)"},
    {"de": 1912.80, "ate": 1915.20, "o_que": "rua do canal à noite (dia 3)"},
    {"de": 1918.75, "ate": 1922.45, "o_que": "Palácio Real à noite (dia 3)"},
]
# fechamento regravado pelo Diego em 23/10/2026 (fonte/narracao/fechamento_v2/, "Narracao fechamento" no Drive)
NARRACAO_FECHAMENTO = [
    {"arq": "fechamento_v2/F_1.m4a", "em": 800, "fala": (0.52, 3.83), "texto": "Amsterdam é de fato encantadora em cada rua que passamos."},
    {"arq": "fechamento_v2/F_2.m4a", "em": 4600, "fala": (0.50, 7.35), "texto": "Nada paga a experiência de passear pelos canais, atravessar cada ponte ou ter medo de ser atropelado por uma bicicleta."},
    {"arq": "fechamento_v2/F_3.m4a", "em": 12050, "fala": (0.12, 8.09), "texto": "Pra gente ficar lá e fazer os passeios, a nossa conta deu 334 euros, contra 553 do hotel. Eu te avisei que o hotel ia ficar mais caro, né?"},
    {"arq": "fechamento_v2/F_4.m4a", "em": 20620, "fala": (0.47, 7.35), "texto": "No total, sem contar a passagem aérea, deu 886 euros para nós dois e uns 443 por pessoa."},
    {"arq": "fechamento_v2/F_5.m4a", "em": 28100, "fala": (0.30, 7.24), "texto": "Outra coisa: compre os ingressos das atrações antes, Museu de Anne Frank e Heineken Experience, porque esgota e vale muito a pena."},
    {"arq": "fechamento_v2/F_6.m4a", "em": 35640, "fala": (0.35, 7.24), "texto": "Se esse vídeo te ajudou de alguma forma, se inscreve, deixa o like aqui e também me segue lá no Instagram, @primeirodiaem, pra não perder nada."},
    {"arq": "fechamento_v2/F_7.m4a", "em": 43130, "fala": (0.45, 4.12), "texto": "Toda cidade tem um primeiro dia, e o próximo é lá em Bruxelas. Te espero lá!"},
]

# ------------------------------------------------------------------------------------------------
# DIAS: corte de troca de dia (fonte), início do dia (relógio), capítulo
DIAS = [
    {"n": 1, "corte": 0.0, "inicio": "14:30", "rotulo": "QUINTA · 12/03"},
    {"n": 2, "corte": 845.875, "inicio": "09:01", "rotulo": "SEXTA · 13/03"},
    {"n": 3, "corte": 1502.62, "inicio": "11:13", "rotulo": "SÁBADO · 14/03"},
]

# GASTOS (fonte em s, valores do Diego). hora = relógio do momento (arquivo do acervo, casado pela fala).
GASTOS = [
    # dia 1
    {"t": "0:21.0", "lugar": "ÔNIBUS 397 · AEROPORTO", "hora": "14:38", "linhas": [("Schiphol → centro × 2 (€ 6,50 cada)", 13.00)], "cat": "transporte", "porque": "Diego (23/10): foram de ônibus do aeroporto e não lembra o valor. Tarifa oficial da linha 397 (Amsterdam Airport Express, Transdev/Connexxion): € 6,50 a viagem. Entra na cena de dentro do ônibus (IMG_1377, 14:38), não durante a fala no aeroporto (pedido do Diego, 23/10)"},
    {"t": "3:15.0", "lugar": "NEW YORK PIZZA", "hora": "16:48", "linhas": [("2 fatias + 1 Coca-Cola", 11.99)], "porque": "Diego: 03:15, 11,99 (2 fatias + 1 coca)"},
    {"t": "6:43.3", "lugar": "MANNEKEN PIS", "hora": "17:36", "linhas": [("Batata pequena + molho", 7.50)], "corrige": 7.15, "porque": "Diego fala € 7,50, mas foi € 7,15 (pedido: corrigir de forma lúdica)"},
    {"t": "7:56.95", "lugar": "TONY'S CHOCOLONELY", "hora": "17:41", "linhas": [("Barras de chocolate", 20.00)], "porque": "Diego: o recibo entra quando ele puxa a alavanca (07:56)"},
    {"t": "9:24.0", "lugar": "HANS EGSTORF", "hora": "18:49", "linhas": [("Stroopwafel com cobertura", 9.50)], "porque": "Diego: 09:24, 9,50"},
    {"t": "10:50.0", "lugar": "THE OLD BELL", "hora": "19:29", "linhas": [("2 cervejas + 1 taça de vinho", 16.60)], "porque": "Diego: 10:50, 16,60"},
    {"t": "13:18.6", "lugar": "McDONALD'S", "hora": "21:21", "linhas": [("McCrispy + lanche da Marina", 12.60)], "porque": "Diego: 13:26, 12,60. Entra 7 s antes, quando ele diz \"Eu pedi o McCrispy\", para não disputar a tela com o rufar e o confete"},
    # dia 2
    {"t": "14:25.0", "lugar": "GUARDA-CHUVA", "hora": "09:06", "linhas": [("Guarda-chuva do hotel", 7.50)], "cat": "outros", "porque": "Diego: 14:27, 7,5 (entra quando ele fala do guarda-chuva)"},
    {"t": "15:42.2", "lugar": "CASA DE ANNE FRANK", "hora": "11:21", "linhas": [("Ingresso × 2 (€ 16 cada)", 32.00)], "cat": "passeios", "porque": "Diego: 15:43, 16 euros por pessoa"},
    {"t": "16:32.5", "lugar": "GVB · TRANSPORTE", "hora": "11:34", "linhas": [("Ticket 48 h × 2 (€ 16 cada)", 32.00)], "cat": "transporte", "fim": 4.1, "porque": "Diego: 16:35, 16 euros; na fala: \"foi 16 euros cada\""},
    {"t": "16:37.7", "lugar": "CAFÉ", "hora": "11:34", "linhas": [("Café na estação", 2.30)], "porque": "Diego: 16:38, cafezinho 2,3"},
    {"t": "18:30.0", "lugar": "BENNY'S CHICKEN", "hora": "12:10", "linhas": [("2 sanduíches + 1 Coca-Cola", 18.48)], "porque": "Diego: 18:30, 18,48"},
    {"t": "19:07.0", "lugar": "RUDI'S ORIGINAL", "hora": "12:18", "linhas": [("Stroopwafel original", 3.50), ("Stroopwafel com chocolate", 4.00)], "porque": "Diego: 19:07, 7,5 (3,50 sem nada e 4 com cobertura)"},
    {"t": "23:00.0", "lugar": "FABEL FRIET", "hora": "17:36", "linhas": [("Batata + maionese e parmesão", 6.95)], "porque": "Diego: 23:00, 6,95"},
    {"t": "23:22.2", "lugar": "HET MOLENTJE", "hora": "17:57", "linhas": [("2 cervejas", 8.00)], "porque": "Diego: 23:22, 8 euros, duas cervejas"},
    {"t": "23:54.0", "lugar": "PIZZA BEPPE", "hora": "19:28", "linhas": [("Pizza, Coca e 2 cervejas", 26.60)], "porque": "Diego: 23:54, 26,60 (1 pizza, 1 coca, 2 cervejas)"},
    {"t": "24:54.0", "lugar": "ALBERT HEIJN", "hora": "20:01", "linhas": [("Refrigerante + docinhos", 9.80)], "porque": "Diego: 24:54, 9,80"},
    # dia 3
    {"t": "28:24.0", "lugar": "FEBO", "hora": "13:12", "linhas": [("Croquete de carne", 3.00)], "porque": "Diego: 28:24, 3 euros"},
    {"t": "28:38.0", "lugar": "FEBO", "hora": "13:15", "linhas": [("Sanduíche de frango", 4.00)], "porque": "Diego: 28:38, 4 euros"},
    {"t": "29:47.0", "lugar": "O'DONNELL'S", "hora": "14:45", "linhas": [("Coca-Cola", 3.90), ("2 copos de cerveja", 9.70)], "porque": "Diego: 29:47, 3,90 coca + 9,70 duas cervejas. Horário ESTIMADO (14:45; o arquivo é de 13:49): na edição do Diego o O'Donnell's vem depois da fachada da Heineken (14:37) e antes da entrada (14:58), e ele pediu um horário que siga essa ordem (23/10)"},
    {"t": "31:17.8", "lugar": "HEINEKEN EXPERIENCE", "hora": "16:52", "linhas": [("Ingresso × 2 (€ 25 cada)", 50.00), ("Garrafa com meu nome", 7.50)], "cat": "passeios", "porque": "Diego: 31:16, 25 euros por pessoa; ingresso mais simples; garrafa 7,5"},
    {"t": None, "chave": "febo2", "lugar": "FEBO · 2ª VEZ", "hora": "21:22", "linhas": [("Sanduíches da última noite", 8.00)], "porque": "Diego (23/10): o 2º FEBO deu 8 euros. Entra no \"passamos no FEBO novamente\" (IMG_2090, 21:22)"},
    {"t": None, "chave": "focaccia", "lugar": "FOCACCIA", "hora": "21:22", "linhas": [("Focaccia para levar", 5.70)], "porque": "Diego (23/10): a focaccia deu 5,70 euros. Entra no \"peguei uma focaccia para levar\" (IMG_2090, 21:22)"},
]
HOTEL_BRL = 3315.08

# ETIQUETAS DE LUGAR (lower third): lugar, bairro/rua (OpenStreetMap ou GPS do acervo) e hora do arquivo
ETIQUETAS = [
    ("0:34.3", "XO HOTEL INNER", "MUSEUMKWARTIER · 15H20"),
    ("1:11.4", "MUSEUMPLEIN", "PRAÇA DOS MUSEUS · 15H51"),
    ("1:51.0", "DANCING HOUSES", "DAMRAK · 16H30"),
    ("3:00.5", "NEW YORK PIZZA", "SPUI · 16H48"),
    ("3:57.5", "PRAÇA DAM", "CENTRUM · 17H10"),
    ("6:16.0", "MANNEKEN PIS", "DAMRAK 41 · 17H36"),
    ("7:12.2", "TONY'S CHOCOLONELY", "OUDEBRUGSTEEG 15 · 17H40"),
    ("8:08.0", "KALVERSTRAAT", "CENTRUM · 18H29"),
    ("9:11.0", "HANS EGSTORF", "SPUISTRAAT 274 · 18H49"),
    ("10:12.0", "THE OLD BELL", "REMBRANDTPLEIN · 19H29"),
    ("11:38.5", "RED LIGHT DISTRICT", "DE WALLEN · 20H55"),
    ("12:48.6", "McDONALD'S", "REGULIERSBREESTRAAT · 21H21"),
    ("15:00.5", "CASA DE ANNE FRANK", "PRINSENGRACHT 263"),
    ("17:02.0", "ALBERT CUYP MARKET", "DE PIJP · 11H57"),
    ("17:59.0", "BENNY'S CHICKEN", "ALBERT CUYPSTRAAT · 12H10"),
    ("18:44.5", "RUDI'S ORIGINAL", "ALBERT CUYPSTRAAT 182 · 12H18"),
    ("20:29.0", "VONDELPARK", "MUSEUMKWARTIER · 15H00"),
    ("22:31.2", "HERENGRACHT × LEIDSEGRACHT", "CINTURÃO DOS CANAIS · 17H19"),
    ("22:45.5", "FABEL FRIET", "RUNSTRAAT · 9 STRAATJES · 17H27"),
    ("23:17.4", "JORDAAN", "E AS 9 STRAATJES"),
    ("23:20.6", "HET MOLENTJE", "GASTHUISMOLENSTEEG · 17H57"),
    ("23:33.2", "PIZZA BEPPE", "LEIDSESTRAAT · 19H28"),
    ("24:08.8", "ALBERT HEIJN", "SUPERMERCADO · 20H01"),
    ("26:10.0", "SARPHATIPARK", "DE PIJP · 12H08"),
    ("27:22.0", "DE PIJP", "BAIRRO RESIDENCIAL · 12H25"),
    ("28:00.6", "FEBO", "DE PIJP · 13H07"),
    ("29:32.0", "O'DONNELL'S", "FERDINAND BOLSTRAAT 5 · 14H45"),  # estimado: ver o gasto do O'Donnell's
    ("29:55.0", "HEINEKEN EXPERIENCE", "STADHOUDERSKADE 78 · 14H58"),
]
DUR_ETIQUETA = {"JORDAAN": 2.9}

# ------------------------------------------------------------------------------------------------


class Mapa:
    """Fonte (s) → saída (ms) pela decupagem; o corpo começa em `base` ms."""

    def __init__(self, edl, base):
        self.seg = edl["manter"]
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
        if t * FPS >= b:  # caiu num trecho cortado: vai para o começo do próximo
            i = min(i + 1, len(self.seg) - 1)
            return self.base + self.ini_out[i] * 1000 / FPS
        return self.base + (self.ini_out[i] + (t * FPS - a)) * 1000 / FPS


def confere_takes(lista, nome):
    """Cada take ≥ 2 s e sem corte de cena dentro (o pedido do Diego de 23/10/2026)."""
    for c in lista:
        dur = c["ate"] - c["de"]
        assert dur >= MIN_TAKE - 1e-6, f"{nome}: take de {dur:.2f} s ({c['o_que']})"
        dentro = [x for x in CENAS if c["de"] < x < c["ate"]]
        assert not dentro, f"{nome}: corte de cena em {dentro} dentro do take {c['o_que']}"


def palavra(tr, texto, depois, antes):
    """Tempo (fonte, s) da palavra `texto` entre `depois` e `antes` na transcrição."""
    for sg in tr["segmentos"]:
        for w in sg["palavras"]:
            if depois <= w["ini"] <= antes and w["p"].lower().strip(".,!?") == texto:
                return w["ini"]
    raise SystemExit(f"palavra {texto!r} não achada entre {depois} e {antes}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guia", action="store_true")
    a = ap.parse_args()
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))
    tr = json.load(open("_tmp/transcricao.json", encoding="utf-8"))
    confere_takes(GANCHO, "gancho")
    confere_takes(FECHAMENTO, "fechamento")

    # momentos do fim do dia 3 (IMG_2090), achados na transcrição
    t_febo2 = palavra(tr, "febo", 1920, 1945)
    t_focaccia = palavra(tr, "focaccia", t_febo2, 1960)
    for g in GASTOS:
        if g.get("chave") == "febo2":
            g["t"] = t_febo2 + 0.3
        elif g.get("chave") == "focaccia":
            g["t"] = t_focaccia - 0.2

    q = lambda ms: round(ms * FPS / 1000)  # noqa: E731
    trechos = []
    audio = []  # para a mixagem: (src_s, out_ms, dur_ms, tipo)
    efeitos = []  # relatório
    takes = []

    def ef(ms, nome, porque, dur=None):
        efeitos.append({"ms": ms, "nome": nome, "porque": porque, "dur": dur})

    # ---------- gancho ----------
    pos = 0
    for c in GANCHO:
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        trechos.append({"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur})
        audio.append({"src": c["de"], "out": pos, "dur": dur, "tipo": "gancho_" + c["som"]})
        takes.append(("gancho", pos, dur, c))
        pos += dur
    G = pos

    # ---------- corpo ----------
    mp = Mapa(edl, G)
    cortes_dia = [d["corte"] for d in DIAS[1:]]
    for (qa, qb), out0 in zip(edl["manter"], mp.ini_out):
        partes = [qa]
        for c in cortes_dia:
            qc = round(c * FPS)
            if qa < qc < qb:
                partes.append(qc)
        partes.append(qb)
        for x, y in zip(partes, partes[1:]):
            de = G + (out0 + x - qa) * 1000 / FPS
            ate = G + (out0 + y - qa) * 1000 / FPS
            tr_ = {"src": round(x * 1000 / FPS), "de": de, "ate": ate}
            if any(abs(y - round(c * FPS)) <= 1 for c in cortes_dia):
                tr_["pagina"] = True
            trechos.append(tr_)
            audio.append({"src": x / FPS, "out": de, "dur": ate - de, "tipo": "corpo"})
    # quadros congelados (imagem parada, som segue)
    for cg in edl.get("congelar", []):
        a0, a1 = mp.ms(cg["de"]), mp.ms(cg["ate"])
        novos = []
        for tr_ in trechos:
            if tr_["de"] < a1 and tr_["ate"] > a0 and "congela" not in tr_:
                if tr_["de"] < a0:
                    novos.append({**tr_, "ate": a0, **({"pagina": False} if tr_.get("pagina") else {})})
                novos.append({"src": round(cg["quadro"] * 1000), "de": max(a0, tr_["de"]), "ate": min(a1, tr_["ate"]), "congela": True})
                if tr_["ate"] > a1:
                    novos.append({**tr_, "src": tr_["src"] + round(a1 - tr_["de"]), "de": a1})
            else:
                novos.append(tr_)
        trechos = novos
        ef(a0, "Quadro congelado (6 quadros)", cg["motivo"], a1 - a0)
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

    ev = []
    zooms = []
    REF = -16

    # ---------- marca, capítulos, placar ----------
    ev.append({"tipo": "placa", "rotulo": "3 DIAS EM", "destino": "AMSTERDAM", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": G + 500, "saida": G + 3900})
    ef(G + 500, "Placa \"3 DIAS EM AMSTERDAM →\" (Chegada + clack)", "Marca do vídeo (doc. do vídeo longo, seção 2): entra sobre a 1ª cena do Dia 1, logo depois do gancho, no lugar de vinheta", 3400)

    def dia_de(t):
        return 3 if t >= DIAS[2]["corte"] else 2 if t >= DIAS[1]["corte"] else 1

    def valor(g):
        return g.get("corrige", sum(v for _, v in g["linhas"]))

    gastos_por_dia = {1: [], 2: [], 3: []}
    for gst in GASTOS:
        gastos_por_dia[dia_de(s(gst["t"]))].append(gst)

    totais_dia = {}
    for d in DIAS:
        cap = (G + 4400) if d["n"] == 1 else mp.ms(d["corte"]) + DUR_PAGINA
        ev.append({"tipo": "placa", "rotulo": d["rotulo"], "destino": f"DIA {d['n']}", "tamanho": "M", "x": 96, "y": 96, "entrada": cap, "saida": cap + 2200})
        ef(cap, f"Placa de capítulo \"DIA {d['n']}\" ({d['rotulo']})", "Início de cada dia (doc., seção 2)" + ("" if d["n"] == 1 else "; entra depois da transição Página (folha virando, 700 ms)"), 2440)
        if d["n"] > 1:
            ef(mp.ms(d["corte"]), "Transição Página + som de folha", f"Troca do dia {d['n'] - 1} para o dia {d['n']} (doc., seção 2)", DUR_PAGINA)
        # Placar (pedido do Diego, 23/10/2026): aparece SÓ quando um gasto é somado e mostra o HORÁRIO real de
        # Amsterdam (hora do arquivo do acervo), não mais o cronômetro desde o início do dia. Liga 200 ms antes do
        # Recibo com o total do dia até ali, soma junto com a moeda do Recibo, fica 3 s e apaga. Gasto que chega antes
        # de o Placar apagar (+2,5 s) soma na mesma aparição. O total continua zerando a cada DIA N.
        aparicoes = []
        soma = 0.0
        for gst in sorted(gastos_por_dia[d["n"]], key=lambda g: mp.ms(g["t"])):
            t_rec = mp.ms(gst["t"])
            em = t_rec + (2600 if "corrige" in gst else 400)
            antes = soma
            soma += valor(gst)
            if aparicoes and t_rec - 200 <= aparicoes[-1]["desligar"] + 2500:
                aparicoes[-1]["valores"].append({"em": em, "tempo": gst["hora"], "gasto": eur(round(soma, 2))})
                aparicoes[-1]["desligar"] = em + 3000
                aparicoes[-1]["lugares"].append(gst["lugar"])
            else:
                aparicoes.append({"ligar": t_rec - 200, "desligar": em + 3000, "lugares": [gst["lugar"]],
                                  "valores": [{"em": t_rec - 200, "tempo": gst["hora"], "gasto": eur(round(antes, 2))},
                                              {"em": em, "tempo": gst["hora"], "gasto": eur(round(soma, 2))}]})
        for ap in aparicoes:
            ev.append({"tipo": "placar", "valores": ap["valores"], "ligar": ap["ligar"], "desligar": ap["desligar"]})
            ef(ap["ligar"], f"Placar do Dia {d['n']}: {ap['valores'][0]['tempo']} · {ap['valores'][-1]['gasto']} ({', '.join(ap['lugares'])})",
               "Pedido do Diego (23/10): só aparece quando um gasto é somado, com o horário real de Amsterdam; liga sem som (a moeda é a do Recibo), soma e apaga 3 s depois", ap["desligar"] - ap["ligar"])
        totais_dia[d["n"]] = round(soma, 2)

    # ---------- etiquetas ----------
    for t, lugar, det in ETIQUETAS:
        ini = mp.ms(t)
        dur = DUR_ETIQUETA.get(lugar, 4.0) * 1000
        ev.append({"tipo": "etiqueta", "lugar": lugar, "detalhe": det, "ini": ini, "fim": ini + dur})
        ef(ini, f"Etiqueta de lugar: {lugar} · {det}", "Lugar novo (doc., seção 2: lugar + bairro + hora; DS 5.4 lower third). Endereço conferido no OpenStreetMap ou no GPS do clipe do acervo", dur)

    # ---------- recibos ----------
    for gst in GASTOS:
        t = mp.ms(gst["t"])
        total = sum(v for _, v in gst["linhas"])
        h, m = gst["hora"].split(":")
        r = {
            "tipo": "recibo",
            "lugar": gst["lugar"],
            "cabecalho": f"DIA {dia_de(s(gst['t']))} · {h}H{m} · AMSTERDAM",
            "linhas": [[it, eur(v)] for it, v in gst["linhas"]],
            "total": eur(total),
            "real": real(total),
            "rodape": RODAPE,
            "ini": t,
            "fim": t + gst.get("fim", 5.5) * 1000,
            "x": 1400,
            "y": 150,
            "escala": 0.72,
        }
        if "corrige" in gst:
            r["correcao"] = {"em": 2600, "nota": "na verdade foi € 7,15 ;)", "cor": "#FF5A4E"}
            r["fim"] = t + 7000
        ev.append(r)
        ef(t, f"Recibo {gst['lugar']}: {eur(total)} (máquina de moeda)" + (" + correção riscada" if "corrige" in gst else ""), gst["porque"], r["fim"] - t)

    # hotel: recibo da hospedagem (fora do Placar do dia: é da estadia inteira)
    t = mp.ms("0:36.0")
    rec_fim = t + 5400
    ev.append({"tipo": "recibo", "lugar": "XO HOTEL INNER", "cabecalho": "HOSPEDAGEM · HOTEIS.COM", "linhas": [["Estadia com café da manhã", ""]], "total": eur(HOTEL_BRL / COTACAO), "real": f"pago {brl(HOTEL_BRL)}, parcelado", "rodape": RODAPE, "ini": t, "fim": rec_fim, "x": 1400, "y": 150, "escala": 0.72})
    ef(t, f"Recibo da hospedagem: {brl(HOTEL_BRL)} = {eur(HOTEL_BRL / COTACAO)}", "Diego: 00:34, recibo durante a fala, valor em euro. Fica fora do Placar do dia 1 (é a estadia inteira); entra no recibo final da viagem", rec_fim - t)
    # print do Diego (22/10/2026), recortado: sai a barra de busca com datas e "1 diária" (não são as da viagem).
    # REV3 (pedido do Diego, 23/10): mais curto, entra logo depois do Recibo e sai antes de ele virar a câmera para
    # mostrar o quarto (a virada começa em 0:46,7 da fonte; a saída de 240 ms termina antes disso)
    t = rec_fim + 300
    fim_print = mp.ms("0:46.3")
    assert fim_print - t >= 3500, (t, fim_print)
    ev.append({"tipo": "print", "arquivo": "print_hotel.png", "endereco": "hoteis.com · XO Hotel Inner", "ini": t, "fim": fim_print, "x": 860, "y": 110, "largura": 960, "alturaJanela": 504, "rolagem": 0})
    ev.append({"tipo": "nota", "titulo": "Link na descrição", "linhas": ["Reservamos pelo Hoteis.com,", "parcelado e com café da manhã."], "ini": t + 500, "fim": fim_print, "x": 860, "y": 735, "largura": 620, "cor": "#3DA9FC", "cor2": "#18C6B3", "icone": "dica"})
    ef(t, "Print da página do hotel no Hoteis.com (janela de navegador surgindo) + nota \"Link na descrição\"", "Pedido do Diego; print enviado por ele em 22/10/2026, recortado para tirar a barra de busca (datas e \"1 diária\" de uma busca nova, não as da viagem). O link é comum, sem afiliado. REV3: sai antes de ele virar a câmera para o quarto", fim_print - t)

    # Tony's: nota de preços
    t = mp.ms("7:58.6")
    ev.append({"tipo": "nota", "titulo": "Preços na Tony's", "linhas": ["Barra pronta: ≈ € 5 cada", "Montar a sua: € 10", "(a gente não montou: caro!)"], "ini": t, "fim": t + 6000, "x": 1352, "y": 470, "largura": 480, "cor": "#8B5CF6", "cor2": "#FF4FA3", "icone": "dica"})
    ef(t, "Nota \"Preços na Tony's\"", "Diego: compraram para comer depois; montar a própria barra custava € 10; as de prateleira, em média € 5", 6000)

    # McCrispy: rufar grave + zoom de tensão + confete murcho
    t_brasil = mp.ms(807.80)
    t_nao = mp.ms(815.18)
    rufar = t_nao - 80 - t_brasil
    ev.append({"tipo": "audio", "arquivo": "AMS_tambor_v2.wav", "em": t_brasil, "volume": 0.0})  # volume definido na mixagem
    zooms.append({"ms": [t_brasil, t_nao - 60, t_nao + 140], "escala": [1.0, 1.10, 1.0], "origem": [48, 42]})
    ev.append({"tipo": "audio", "arquivo": "AMS_confete_murcho_v1.wav", "em": t_nao + 380, "volume": 0.0})
    ev.append({"tipo": "confete", "em": t_nao + 380, "x": 1690, "y": 600})
    ef(t_brasil, f"Rufar grave ({rufar / 1000:.2f} s) + zoom lento de tensão (100% → 110%)", "Pedido do Diego (23/10): tambores mais graves, com ar de mistério, no mesmo andamento do v1 (21 → 29 toques/s); para logo antes do \"não\"; o zoom volta a 100% no \"não\"", rufar)
    ef(t_nao + 380, "Confete murcho (som + lança-confete que falha)", "Pedido do Diego (23/10), no lugar dos fogos: \"um confete estourado, daqueles murchos que palhaço estoura\". A cordinha é puxada, sai um \"pfft\", a língua de sogra murcha e o papel cai devagar, no canto direito (o Diego está no centro)", 2300)

    # Anne Frank: nota
    t = mp.ms("15:44.6")
    ev.append({"tipo": "nota", "titulo": "Compre antes", "linhas": ["Só online, no site oficial.", "Abre toda terça, às 10h,", "para 6 semanas depois.", "Esgota rápido! Link na descrição ↓"], "ini": t, "fim": t + 7500, "x": 1252, "y": 470, "largura": 580, "cor": "#FF5A4E", "cor2": "#FF9F1C", "icone": "alerta"})
    ef(t, "Nota \"Compre antes\" (Anne Frank)", "Pedido do Diego. Regra conferida no site oficial (annefrank.org, 21/10/2026): ingresso só online, liberado toda terça às 10h para 6 semanas depois", 7500)

    # Het Molentje: nota de temperatura
    t = mp.ms("23:23.8")
    ev.append({"tipo": "nota", "titulo": "Fugindo do vento", "linhas": ["10 °C, sensação de 2 °C", "por causa do vento"], "ini": t, "fim": t + 5000, "x": 1352, "y": 410, "largura": 480, "cor": "#3DA9FC", "cor2": "#8B5CF6", "icone": "alerta"})
    ef(t, "Nota \"Fugindo do vento: 10 °C, sensação de 2 °C\"", "Diego: entraram no Het Molentje para tomar uma cerveja e fugir do vento frio (registro dele)", 5000)

    # Praça dos museus: placa + quadro
    t = mp.ms("19:32.6")
    fim_q = mp.ms("19:53.0")
    ev.append({"tipo": "placa", "rotulo": "MUSEUMPLEIN", "destino": "PRAÇA DOS MUSEUS", "tamanho": "M", "x": 96, "y": 200, "entrada": t, "saida": fim_q})
    ev.append({"tipo": "quadro", "linhas": [{"em": mp.ms(1175.39), "nome": "RIJKSMUSEUM", "complemento": "MUSEU NACIONAL"}, {"em": mp.ms(1184.20), "nome": "VAN GOGH MUSEUM"}, {"em": mp.ms(1187.35), "nome": "MOCO MUSEUM", "complemento": "ARTE MODERNA"}], "fim": fim_q, "x": 96, "y": 380, "escala": 0.75})
    ef(t, "Placa \"PRAÇA DOS MUSEUS\" + Quadro com os 3 museus acendendo um a um", "Pedido do Diego: a lista aparece aos poucos, quando cada museu é falado (Rijksmuseum, Van Gogh, Moco)", fim_q - t)

    # De Pijp: bilhete das bikes
    t = mp.ms("27:26.2")
    ev.append({"tipo": "bilhete", "texto": "bairro residencial…|e bike sem fim!", "marca": "circulo", "x": 1330, "y": 130, "escala": 0.8, "entrada": t, "saida": t + 3400})
    ef(t, "Bilhete na letra do Diego: \"bairro residencial… e bike sem fim!\" (círculo de caneta)", "Pedido do Diego (nota das bikes, \"melhore isso\"): opinião com humor vira Bilhete (DS 2.4), escrito sobre o plano das bicicletas estacionadas", 4400)

    # Heineken: selo vale a pena + nota
    t = mp.ms(1876.1)
    ev.append({"tipo": "ticket", "variante": "vale", "palavra": "VALE A PENA", "micro": "HEINEKEN EXPERIENCE · DIA 3", "x": 110, "y": 760, "escala": 0.72, "entrada": t, "saida": t + 4600})
    ef(t, "Selo VALE A PENA (Ticket VALE, Subida + ding)", "Pedido do Diego, no \"valeu a pena\" da Heineken Experience", 4840)
    t = mp.ms("31:20.0")
    ev.append({"tipo": "nota", "titulo": "Compre antes", "linhas": ["Ingresso online, com horário:", "os horários esgotam.", "Link na descrição ↓"], "ini": t, "fim": t + 6000, "x": 1292, "y": 520, "largura": 540, "cor": "#FF5A4E", "cor2": "#FF9F1C", "icone": "alerta"})
    ef(t, "Nota \"Compre antes\" (Heineken)", "Pedido do Diego: comprar antes porque esgota", 6000)

    # ---------- chamadas ----------
    for t, dur, porque in [("2:04.4", 4.5, "1ª de 3 (≈ 2–3 min), na montagem dos canais, sem fala"), ("17:30.0", 4.5, "2ª de 3 (≈ metade do vídeo), na montagem do Albert Cuyp, sem fala")]:
        ini = mp.ms(t)
        ev.append({"tipo": "instagram", "ini": ini, "fim": ini + dur * 1000})
        ef(ini, "Chamada SEGUE NO INSTAGRAM @primeirodiaem", porque + ". Texto \"Instagram\" por extenso: a Meta proíbe abreviar o nome", dur * 1000)
    t = mp.ms("9:55.0")
    ev.append({"tipo": "like", "entrada": t, "saida": t + 3900})
    ef(t, "Animação \"DEIXA O LIKE E SE INSCREVE\" (clique + ding)", "Doc., seção 2: versão curta, sem fala, em 30–40% do vídeo, sobre a montagem da Munttoren e do bonde", 4140)

    # ---------- fechamento (relógio do fechamento, ms; a fala de cada bloco está em NARRACAO_FECHAMENTO) ----------
    f = B_fim
    total_gastos = sum(valor(g) for g in GASTOS)
    hotel = HOTEL_BRL / COTACAO
    cat = {"comida": 0.0, "passeios": 0.0, "transporte": 0.0, "outros": 0.0}
    for g in GASTOS:
        cat[g.get("cat", "comida")] += valor(g)
    assert abs(sum(cat.values()) - total_gastos) < 0.005
    total = total_gastos + hotel
    # REV3: tempos do fechamento regravado (F3 "a nossa conta deu" em +13,5 s; F5 "vale muito a pena" em +33,9 s;
    # F6 "se inscreve, deixa o like" em +37,0 s e "me segue lá no Instagram" em +39,3 s; F7 em +43,1 s)
    ev.append({"tipo": "recibo", "lugar": "3 DIAS EM AMSTERDAM", "cabecalho": "12 A 14/03 · 2 PESSOAS · SEM PASSAGEM", "linhas": [["Hospedagem", eur(hotel)], ["Comida e bebida", eur(cat["comida"])], ["Passeios", eur(cat["passeios"])], ["Transporte", eur(cat["transporte"])], ["Guarda-chuva", eur(cat["outros"])]], "total": eur(total), "real": f"{eur(total / 2)} por pessoa ≈ {brl(total / 2 * COTACAO)}", "rodape": RODAPE, "ini": f + 13400, "fim": f + 27900, "x": 1360, "y": 96, "escala": 0.78})
    ef(f + 13400, f"Recibo da viagem: {eur(total)} para 2 ({eur(total / 2)} por pessoa)", "Doc., seção 2: fechamento com o total da viagem (2 pessoas e por pessoa, € e R$). Entra no \"a nossa conta deu\" (F3) e fica até o fim do total (F4). Responde à pergunta do gancho", 14500)
    ev.append({"tipo": "nota", "titulo": "Compre antes", "linhas": ["Casa de Anne Frank", "Heineken Experience", "Esgotam! Links na descrição ↓"], "ini": f + 28600, "fim": f + 33600, "x": 1292, "y": 470, "largura": 540, "cor": "#FF5A4E", "cor2": "#FF9F1C", "icone": "alerta"})
    ef(f + 28600, "Nota \"Compre antes\" (Anne Frank e Heineken)", "A dica do F5 (\"compre os ingressos das atrações antes... porque esgota\"), com o mesmo componente das notas do corpo", 5000)
    ev.append({"tipo": "bilhete", "texto": "vale muito a pena!", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": f + 33900, "saida": f + 37000})
    ef(f + 33900, "Bilhete do veredito: \"vale muito a pena!\" + ✓", "Doc., seção 2: Bilhete com o veredito no fechamento, no \"vale muito a pena\" do F5 (o F2 novo não tem mais o veredito), sobre os dois rindo debaixo do guarda-chuva", 3100)
    ev.append({"tipo": "like", "entrada": f + 36400, "saida": f + 39200})
    ef(f + 36400, "Animação \"DEIXA O LIKE E SE INSCREVE\" (2ª vez)", "Doc., seção 2: like e inscrição também no fechamento, no \"se inscreve, deixa o like aqui\" (F6)", 3040)
    ev.append({"tipo": "instagram", "ini": f + 39450, "fim": f + 42400})
    ef(f + 39450, "Chamada SEGUE NO INSTAGRAM (3ª vez)", "Doc., seção 2: 3ª chamada, no \"me segue lá no Instagram, arroba primeirodiaem\" (F6)", 2950)
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": f + 42900, "saida": F_fim - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": f + 42900 + 400, "relDb": -12})
    ef(f + 42900, "Placa de fechamento \"TODA CIDADE TEM UM PRIMEIRO DIA.\" + Nascer do 1º", "DS 4.3 e 5.4 (aprovada pelo Diego em 23/10): entra com o \"Toda cidade tem um primeiro dia\" (F7)", F_fim - f - 42900)
    ev.append({"tipo": "telafinal", "ini": F_fim, "proximo": "bruxelas"})
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: bruxelas →\")", "Doc., seção 2 e amostra aprovada em 16/10/2026", TELA_FINAL)

    # narrações no relógio do vídeo final (ms): onde o arquivo começa a tocar e o trecho de fala
    narr = []
    for base, lista in [(0, NARRACAO_GANCHO), (B_fim, NARRACAO_FECHAMENTO)]:
        for n in lista:
            f0, f1 = n["fala"]
            narr.append({"arq": n["arq"], "fala_ini": base + n["em"], "fala_fim": base + n["em"] + (f1 - f0) * 1000, "arq_ini_s": f0, "arq_fim_s": f1, "texto": n["texto"]})
    for a_, b_ in zip(narr, narr[1:]):
        assert a_["fala_fim"] + 150 <= b_["fala_ini"], (a_["texto"][:30], b_["texto"][:30])
    assert narr[2]["fala_fim"] < G and narr[-1]["fala_fim"] < F_fim - 300

    # ---------- guia de narração (versão de trabalho) ----------
    if a.guia:
        frases = [{"ini": n["fala_ini"], "fim": n["fala_fim"], "texto": n["texto"]} for n in narr]
        ev.append({"tipo": "guia", "inicio": 0, "fim": G, "frases": frases})
        ev.append({"tipo": "guia", "inicio": B_fim, "fim": F_fim, "frases": frases})

    # os sons próprios do vídeo (rufar, confete) entram na mixagem (rev3/mixar_rev3.py), não no render
    props = {"video": "http://127.0.0.1:8787/proxy1080.mp4", "duracao": duracao, "trechos": trechos, "eventos": [e for e in ev if e["tipo"] != "audio"], "zooms": zooms, "refLufs": REF}
    json.dump(props, open("rev3/props_rev3.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio,
               "narracoes": narr, "sons": [e for e in ev if e["tipo"] == "audio"], "rufar_ms": rufar,
               "dias_ms": [mp.ms(d["corte"]) for d in DIAS[1:]],
               "totais": {"gastos": round(total_gastos, 2), "hotel": round(hotel, 2), "total": round(total, 2), "por_pessoa": round(total / 2, 2), **{k: round(v, 2) for k, v in cat.items()}, "dias": totais_dia}},
              open("rev3/linha_do_tempo_rev3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(ms):
        return f"{int(ms // 60000):02d}:{(ms % 60000) / 1000:04.1f}"

    linhas = ["# REV3 · Efeitos visuais e sonoros (vlog de Amsterdam)", "",
              "Gerado por `rev3/montar_rev3.py`. Minutos no **vídeo final** (com gancho e decupagem). Cores dos efeitos: camada de efeitos (decisão do Diego, 21/10/2026); objetos da marca nas cores do DS.", "",
              "| Entra | Dura | Efeito | Por quê |", "|---|---:|---|---|"]
    for e in sorted(efeitos, key=lambda x: x["ms"]):
        d = f"{e['dur'] / 1000:.1f} s" if e["dur"] else ""
        linhas.append(f"| {mmss(e['ms'])} | {d} | {e['nome']} | {e['porque']} |")
    open("rev3/efeitos_rev3.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")

    lt = ["# REV3 · Takes do gancho e do fechamento", "",
          f"Pedido do Diego (23/10/2026): cada take com pelo menos {MIN_TAKE:.0f} s. Tempos no vídeo final; a fonte é o export `1016_sem_musica.mp4`. Nenhum take tem corte de cena dentro (conferido contra os cortes detectados na fonte, lista `CENAS` do script).", "",
          "| Bloco | Entra | Dura | Fonte | Plano |", "|---|---|---:|---|---|"]
    def seg(ms):
        return f"{ms / 1000:.2f}".replace(".", ",") + " s"

    for bloco, ini, dur, c in takes:
        lt.append(f"| {bloco} | {mmss(ini)} | {seg(dur)} | {mmss(c['de'] * 1000)}–{mmss(c['ate'] * 1000)} | {c['o_que']} |")
    menor = min(d for _, _, d, _ in takes) / 1000
    lt += ["", f"Menor take: **{seg(menor * 1000)}**. Na REV1 havia 3 takes abaixo de 2 s escondidos dentro dos trechos: 1,24 s (bandeira do hotel De L'Europe, no fim do plano dos canais do fechamento), 0,18 s (ponte com flores, no gancho) e 0,12 s (chafariz do Vondelpark, no fechamento).", ""]
    lt += ["## Narrações (como foram ditas)", "", "| Bloco | Fala no vídeo | Texto (transcrição automática, a confirmar na escuta) |", "|---|---|---|"]
    for n in narr:
        lt.append(f"| {n['arq']} | {mmss(n['fala_ini'])}–{mmss(n['fala_fim'])} | {n['texto']} |")
    open("rev3/takes_rev3.md", "w", encoding="utf-8").write("\n".join(lt) + "\n")

    print(f"gancho {G / 1000:.2f} s · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} ({(F_fim - B_fim) / 1000:.1f} s) · total {mmss(duracao)}")
    print(f"trechos {len(trechos)} · eventos {len(ev)} · rufar {rufar / 1000:.2f} s · menor take {menor:.2f} s")
    print(f"gastos {eur(total_gastos)} · hotel {eur(hotel)} · total {eur(total)} · por pessoa {eur(total / 2)} ({brl(total / 2 * COTACAO)}) · {', '.join(f'{k} {eur(v)}' for k, v in cat.items())} · dias {totais_dia}")
    print(f"FEBO 2: fonte {t_febo2:.2f} s · focaccia: fonte {t_focaccia:.2f} s")


if __name__ == "__main__":
    sys.exit(main())
