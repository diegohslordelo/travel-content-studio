"""Montagem da REV1 do vlog de Amsterdam (vídeo longo do YouTube, 16:9).

Lê a decupagem (`edl_rev1.json`) e as decisões abaixo (todas no tempo da FONTE, o export do Diego), converte
para o relógio do vídeo final e escreve:
  rev1/props_rev1.json        props da composição `VideoLongo` (Remotion)
  rev1/linha_do_tempo_rev1.json  trechos de áudio para a mixagem (fonte → saída), narrações e música
  rev1/efeitos_rev1.md        relatório de cada efeito: minuto em que entra e por quê

Roda de reels/ams-yt:  python rev1/montar_rev1.py [--guia]
--guia liga o contador e o texto da narração na tela (versão de trabalho para gravar e aprovar).

Ordem do vídeo: gancho (clipes de vários momentos + narração a gravar) → corpo (decupado) → fechamento
(clipes + narração a gravar) → tela final de 20 s. Valores: todos do registro do Diego (21/10/2026); o real é
convertido pela PTAX de venda de 12/03/2026 (Banco Central), € 1 = R$ 5,9978.
"""
import argparse
import json
import re
from bisect import bisect_right
from decimal import ROUND_HALF_UP, Decimal

FPS = 24
COTACAO = 5.9978
RODAPE = "cotação € 1 = R$ 5,9978 · PTAX 12/03/2026"
TELA_FINAL = 20000
DUR_PAGINA = 700


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
# GANCHO: 8 momentos (fonte em s) e a narração a gravar (relógio do gancho, ms). Linhas reais: Marina
# ("Gente, meu cabelo!") e Diego ("Bebi quatro, estou realizado."). Nos outros clipes o som real fica baixo.
GANCHO = [
    {"de": 135.2, "ate": 138.0, "o_que": "canal com as casas tortas (Damrak, dia 1)", "som": "baixo"},
    {"de": 211.9, "ate": 214.1, "o_que": "vento no cabelo da Marina: \"Gente, meu cabelo!\"", "som": "fala"},
    {"de": 846.9, "ate": 849.7, "o_que": "chuva, guarda-chuva do hotel (dia 2)", "som": "baixo"},
    {"de": 1646.2, "ate": 1648.4, "o_que": "bicicletas em De Pijp (dia 3)", "som": "baixo"},
    {"de": 476.4, "ate": 478.8, "o_que": "alavanca da parede de chocolate na Tony's", "som": "baixo"},
    {"de": 1159.6, "ate": 1162.6, "o_que": "stroopwafel do Rudi's: \"Surreal.\"", "som": "fala"},
    {"de": 1865.3, "ate": 1867.7, "o_que": "Heineken: \"Bebi quatro, estou realizado.\"", "som": "fala"},
    {"de": 1356.5, "ate": 1359.8, "o_que": "ponte com flores e bicicleta vermelha (Leidsestraat)", "som": "baixo"},
    {"de": 1913.0, "ate": 1918.4, "o_que": "canais à noite (dia 3)", "som": "baixo"},
]
NARRACAO_GANCHO = [
    (200, 2600, "Três dias em Amsterdam."),
    (5100, 10500, "Vento com sensação térmica de 2 graus, chuva… e bicicleta pra todo lado."),
    (10400, 12900, "Chocolate, stroopwafel quentinho…"),
    (18300, 25600, "E eu anotei cada euro que a gente gastou. No final, eu te mostro quanto deu tudo, e se vale a pena."),
]

# FECHAMENTO: clipes sem fala depois do último plano do Diego; narração a gravar (relógio do fechamento, ms)
FECHAMENTO = [
    {"de": 1904.0, "ate": 1912.4, "o_que": "pôr do sol nos canais (dia 3)"},
    {"de": 594.2, "ate": 599.4, "o_que": "Munttoren no fim da tarde (dia 1)"},
    {"de": 1245.0, "ate": 1247.6, "o_que": "chafariz do Vondelpark (dia 2)"},
    {"de": 1175.0, "ate": 1177.8, "o_que": "Rijksmuseum (dia 2)"},
    {"de": 294.2, "ate": 302.2, "o_que": "Palácio Real na Praça Dam (dia 1)"},
    {"de": 124.2, "ate": 129.4, "o_que": "canais com as casas tortas (dia 1)"},
    {"de": 1313.0, "ate": 1315.6, "o_que": "barco no canal (dia 2)"},
    {"de": 1919.0, "ate": 1922.3, "o_que": "Palácio Real à noite (dia 3)"},
]
NARRACAO_FECHAMENTO = [
    (400, 9000, "Fechando a conta: em três dias, a gente gastou € 307 com comida, passeios e transporte, e € 553 de hotel."),
    (9200, 15600, "No total, € 860 para dois: uns € 430 por pessoa, perto de R$ 2.580 cada, sem a passagem."),
    (16000, 22200, "Vale a pena? Vale. Mas leve casaco para o vento e compre a Anne Frank e a Heineken antes."),
    (22600, 26600, "Se esse vídeo te ajudou, deixa o like e se inscreve."),
    (27000, 30600, "E me segue no Instagram: @primeirodiaem."),
    (31200, 36400, "Toda cidade tem um primeiro dia. O próximo é em Bruxelas."),
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
    {"t": "3:15.0", "lugar": "NEW YORK PIZZA", "hora": "16:48", "linhas": [("2 fatias + 1 Coca-Cola", 11.99)], "porque": "Diego: 03:15, 11,99 (2 fatias + 1 coca)"},
    {"t": "6:43.3", "lugar": "MANNEKEN PIS", "hora": "17:36", "linhas": [("Batata pequena + molho", 7.50)], "corrige": 7.15, "porque": "Diego fala € 7,50, mas foi € 7,15 (pedido: corrigir de forma lúdica)"},
    {"t": "7:56.95", "lugar": "TONY'S CHOCOLONELY", "hora": "17:41", "linhas": [("Barras de chocolate", 20.00)], "porque": "Diego: o recibo entra quando ele puxa a alavanca (07:56)"},
    {"t": "9:24.0", "lugar": "HANS EGSTORF", "hora": "18:49", "linhas": [("Stroopwafel com cobertura", 9.50)], "porque": "Diego: 09:24, 9,50"},
    {"t": "10:50.0", "lugar": "THE OLD BELL", "hora": "19:29", "linhas": [("2 cervejas + 1 taça de vinho", 16.60)], "porque": "Diego: 10:50, 16,60"},
    {"t": "13:18.6", "lugar": "McDONALD'S", "hora": "21:21", "linhas": [("McCrispy + lanche da Marina", 12.60)], "porque": "Diego: 13:26, 12,60. Entra 7 s antes, quando ele diz \"Eu pedi o McCrispy\", para não disputar a tela com o rufar e os fogos"},
    # dia 2
    {"t": "14:25.0", "lugar": "GUARDA-CHUVA", "hora": "09:06", "linhas": [("Guarda-chuva do hotel", 7.50)], "porque": "Diego: 14:27, 7,5 (entra quando ele fala do guarda-chuva)"},
    {"t": "15:42.2", "lugar": "CASA DE ANNE FRANK", "hora": "11:21", "linhas": [("Ingresso × 2 (€ 16 cada)", 32.00)], "porque": "Diego: 15:43, 16 euros por pessoa"},
    {"t": "16:32.5", "lugar": "GVB · TRANSPORTE", "hora": "11:34", "linhas": [("Ticket 48 h × 2 (€ 16 cada)", 32.00)], "fim": 4.1, "porque": "Diego: 16:35, 16 euros; na fala: \"foi 16 euros cada\""},
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
    {"t": "29:47.0", "lugar": "O'DONNELL'S", "hora": "13:49", "linhas": [("Coca-Cola", 3.90), ("2 copos de cerveja", 9.70)], "porque": "Diego: 29:47, 3,90 coca + 9,70 duas cervejas"},
    {"t": "31:17.8", "lugar": "HEINEKEN EXPERIENCE", "hora": "16:52", "linhas": [("Ingresso × 2 (€ 25 cada)", 50.00), ("Garrafa com meu nome", 7.50)], "porque": "Diego: 31:16, 25 euros por pessoa; ingresso mais simples; garrafa 7,5"},
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
    ("29:32.0", "O'DONNELL'S", "FERDINAND BOLSTRAAT 5 · 13H49"),
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guia", action="store_true")
    a = ap.parse_args()
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))

    q = lambda ms: round(ms * FPS / 1000)  # noqa: E731
    trechos = []
    audio = []  # para a mixagem: (src_s, out_ms, dur_ms, tipo)
    efeitos = []  # relatório

    def ef(ms, nome, porque, dur=None):
        efeitos.append({"ms": ms, "nome": nome, "porque": porque, "dur": dur})

    # ---------- gancho ----------
    pos = 0
    for c in GANCHO:
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        trechos.append({"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur})
        audio.append({"src": c["de"], "out": pos, "dur": dur, "tipo": "gancho_" + c["som"]})
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
            tr = {"src": round(x * 1000 / FPS), "de": de, "ate": ate}
            if any(abs(y - round(c * FPS)) <= 1 for c in cortes_dia):
                tr["pagina"] = True
            trechos.append(tr)
            audio.append({"src": x / FPS, "out": de, "dur": ate - de, "tipo": "corpo"})
    # quadros congelados (imagem parada, som segue)
    for cg in edl.get("congelar", []):
        a0, a1 = mp.ms(cg["de"]), mp.ms(cg["ate"])
        novos = []
        for tr in trechos:
            if tr["de"] < a1 and tr["ate"] > a0 and "congela" not in tr:
                if tr["de"] < a0:
                    novos.append({**tr, "ate": a0, **({"pagina": False} if tr.get("pagina") else {})})
                novos.append({"src": round(cg["quadro"] * 1000), "de": max(a0, tr["de"]), "ate": min(a1, tr["ate"]), "congela": True})
                if tr["ate"] > a1:
                    novos.append({**tr, "src": tr["src"] + round(a1 - tr["de"]), "de": a1})
            else:
                novos.append(tr)
        trechos = novos
        ef(a0, "Quadro congelado (6 quadros)", cg["motivo"], a1 - a0)
    B_fim = G + mp.dur_q * 1000 / FPS

    # ---------- fechamento ----------
    pos = B_fim
    for i, c in enumerate(FECHAMENTO):
        dur = q((c["ate"] - c["de"]) * 1000) * 1000 / FPS
        tr = {"src": round(c["de"] * 1000), "de": pos, "ate": pos + dur}
        if i == len(FECHAMENTO) - 1:
            tr["pagina"] = True
        trechos.append(tr)
        audio.append({"src": c["de"], "out": pos, "dur": dur, "tipo": "fechamento"})
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

    gastos_por_dia = {1: [], 2: [], 3: []}
    for gst in GASTOS:
        t = s(gst["t"])
        dia = 3 if t >= DIAS[2]["corte"] else 2 if t >= DIAS[1]["corte"] else 1
        gastos_por_dia[dia].append(gst)

    for d in DIAS:
        cap = (G + 4400) if d["n"] == 1 else mp.ms(d["corte"]) + DUR_PAGINA
        ev.append({"tipo": "placa", "rotulo": d["rotulo"], "destino": f"DIA {d['n']}", "tamanho": "M", "x": 96, "y": 96, "entrada": cap, "saida": cap + 2200})
        ef(cap, f"Placa de capítulo \"DIA {d['n']}\" ({d['rotulo']})", "Início de cada dia (doc., seção 2)" + ("" if d["n"] == 1 else "; entra depois da transição Página (folha virando, 700 ms)"), 2440)
        if d["n"] > 1:
            ef(mp.ms(d["corte"]), "Transição Página + som de folha", f"Troca do dia {d['n'] - 1} para o dia {d['n']} (doc., seção 2)", DUR_PAGINA)
        ligar = cap + 2600
        fim_dia = (mp.ms(DIAS[d["n"]]["corte"]) if d["n"] < 3 else B_fim) - 300
        h0, m0 = map(int, d["inicio"].split(":"))
        marcos = []  # (ms, hora "HH:MM", gasto a somar)
        for gst in gastos_por_dia[d["n"]]:
            em = mp.ms(gst["t"]) + (2600 if "corrige" in gst else 400)
            marcos.append((em, gst["hora"], gst.get("corrige", sum(v for _, v in gst["linhas"]))))
        for t, _lugar, det in ETIQUETAS:
            hh = re.search(r"(\d\d)H(\d\d)$", det)
            if hh and dia_de(s(t)) == d["n"]:
                marcos.append((mp.ms(t) + 600, f"{hh.group(1)}:{hh.group(2)}", 0.0))
        marcos.sort()
        valores = [{"em": ligar, "tempo": "+00:00", "gasto": eur(0)}]
        soma = 0.0
        ultimo_som = -1e9
        for em, hora, g in marcos:
            if em < ligar:
                em = ligar + 300
            h, m = map(int, hora.split(":"))
            dm = max(0, (h * 60 + m) - (h0 * 60 + m0))
            soma += g
            tempo = f"+{dm // 60:02d}:{dm % 60:02d}"
            if tempo == valores[-1]["tempo"] and g == 0:
                continue
            valores.append({"em": em, "tempo": tempo, "gasto": eur(round(soma, 2))})
            if g == 0 and em - ultimo_som >= 1500:
                ev.append({"tipo": "som", "nome": "tick", "em": em, "relDb": -14})
            ultimo_som = em
        ev.append({"tipo": "placar", "valores": valores, "ligar": ligar, "desligar": fim_dia})
        ef(ligar, f"Placar do Dia {d['n']} (liga sem som; soma a cada recibo)", f"Doc., seção 2: Placar em todos os dias, zerando a cada DIA N. Tempo desde {d['inicio']} (hora do 1º arquivo do dia); gira a cada lugar novo (tick) e a cada gasto (moeda). Total do dia: {eur(round(soma, 2))}", fim_dia - ligar)

    # ---------- etiquetas ----------
    for t, lugar, det in ETIQUETAS:
        ini = mp.ms(t)
        dur = DUR_ETIQUETA.get(lugar, 4.0) * 1000
        ev.append({"tipo": "etiqueta", "lugar": lugar, "detalhe": det, "ini": ini, "fim": ini + dur})
        ef(ini, f"Etiqueta de lugar: {lugar} · {det}", "Lugar novo (doc., seção 2: lugar + bairro + hora; DS 5.4 lower third). Endereço conferido no OpenStreetMap ou no GPS do clipe do acervo", dur)

    # ---------- recibos ----------
    for gst in GASTOS:
        t = mp.ms(gst["t"])
        dia = 3 if s(gst["t"]) >= DIAS[2]["corte"] else 2 if s(gst["t"]) >= DIAS[1]["corte"] else 1
        total = sum(v for _, v in gst["linhas"])
        h, m = gst["hora"].split(":")
        r = {
            "tipo": "recibo",
            "lugar": gst["lugar"],
            "cabecalho": f"DIA {dia} · {h}H{m} · AMSTERDAM",
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
    ev.append({"tipo": "recibo", "lugar": "XO HOTEL INNER", "cabecalho": "HOSPEDAGEM · HOTEIS.COM", "linhas": [["Estadia com café da manhã", ""]], "total": eur(HOTEL_BRL / COTACAO), "real": f"pago {brl(HOTEL_BRL)}, parcelado", "rodape": RODAPE, "ini": t, "fim": t + 6000, "x": 1400, "y": 150, "escala": 0.72})
    ef(t, f"Recibo da hospedagem: {brl(HOTEL_BRL)} = {eur(HOTEL_BRL / COTACAO)}", "Diego: 00:34, recibo durante a fala, valor em euro. Fica fora do Placar do dia 1 (é a estadia inteira); entra no recibo final da viagem", 6000)
    t = mp.ms("0:43.0")
    ev.append({"tipo": "print", "arquivo": "print_hotel_PENDENTE.png", "endereco": "hoteis.com · XO Hotel Inner", "ini": t, "fim": t + 6500, "x": 860, "y": 110, "largura": 960, "alturaJanela": 560, "rolagem": 220})
    ev.append({"tipo": "nota", "titulo": "Link na descrição", "linhas": ["Reservamos pelo Hoteis.com,", "parcelado e com café da manhã."], "ini": t + 700, "fim": t + 6500, "x": 860, "y": 735, "largura": 620, "cor": "#3DA9FC", "cor2": "#18C6B3", "icone": "dica"})
    ef(t, "Print da página do hotel no Hoteis.com (janela de navegador surgindo) + nota \"Link na descrição\"", "Pedido do Diego. Mostrar o print de um site num vlog não fere as regras de monetização do YouTube (é contexto do conteúdo original). O site bloqueia captura automática: na prévia o espaço está marcado e o print vem do Diego", 6500)

    # Manneken Pis: correção
    # Tony's: nota de preços
    t = mp.ms("7:58.6")
    ev.append({"tipo": "nota", "titulo": "Preços na Tony's", "linhas": ["Barra pronta: ≈ € 5 cada", "Montar a sua: € 10", "(a gente não montou: caro!)"], "ini": t, "fim": t + 6000, "x": 1352, "y": 470, "largura": 480, "cor": "#8B5CF6", "cor2": "#FF4FA3", "icone": "dica"})
    ef(t, "Nota \"Preços na Tony's\"", "Diego: compraram para comer depois; montar a própria barra custava € 10; as de prateleira, em média € 5", 6000)

    # McCrispy: rufar + zoom de tensão + fogos murchos
    t_brasil = mp.ms(807.80)
    t_nao = mp.ms(815.18)
    rufar = t_nao - 80 - t_brasil
    ev.append({"tipo": "audio", "arquivo": "AMS_tambor_v1.wav", "em": t_brasil, "volume": 0.0})  # volume definido na mixagem
    zooms.append({"ms": [t_brasil, t_nao - 60, t_nao + 140], "escala": [1.0, 1.10, 1.0], "origem": [48, 42]})
    ev.append({"tipo": "audio", "arquivo": "AMS_fogos_murchos_v1.wav", "em": t_nao + 320, "volume": 0.0})
    ev.append({"tipo": "fogos", "em": t_nao + 320, "x": 1450, "y": 300, "altura": 520})
    ef(t_brasil, f"Rufar de tambores ({rufar / 1000:.2f} s) + zoom lento de tensão (100% → 110%)", "Pedido do Diego: rufar que para logo antes do \"não\". Mantive a mordida e encurtei a mastigação (7,5 s → ~3,9 s) para o rufar caber; o zoom volta a 100% no \"não\"", rufar)
    ef(t_nao + 320, "Fogos murchos (som + animação colorida)", "Pedido do Diego: logo depois do \"não\", fogos que dão errado: o rojão sobe, perde força, dá um \"puf\" e as faíscas murcham", 2450)

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

    # ---------- fechamento: recibo da viagem, bilhete, like, instagram, placa + nascer, tela final ----------
    f = B_fim
    total_gastos = sum(sum(v for _, v in gst["linhas"]) - (sum(v for _, v in gst["linhas"]) - gst["corrige"] if "corrige" in gst else 0) for gst in GASTOS)
    hotel = HOTEL_BRL / COTACAO
    comida = sum(sum(v for _, v in g["linhas"]) - (sum(v for _, v in g["linhas"]) - g["corrige"] if "corrige" in g else 0) for g in GASTOS if g["lugar"] not in ("CASA DE ANNE FRANK", "HEINEKEN EXPERIENCE", "GVB · TRANSPORTE", "GUARDA-CHUVA"))
    passeios = 32.00 + 57.50
    transporte = 32.00
    outros = 7.50
    assert abs(comida + passeios + transporte + outros - total_gastos) < 0.005, (comida, total_gastos)
    total = total_gastos + hotel
    ev.append({"tipo": "recibo", "lugar": "3 DIAS EM AMSTERDAM", "cabecalho": "12 A 14/03 · 2 PESSOAS · SEM PASSAGEM", "linhas": [["Hospedagem", eur(hotel)], ["Comida e bebida", eur(comida)], ["Passeios", eur(passeios)], ["Transporte", eur(transporte)], ["Guarda-chuva", eur(outros)]], "total": eur(total), "real": f"{eur(total / 2)} por pessoa ≈ {brl(total / 2 * COTACAO)}", "rodape": RODAPE, "ini": f + 700, "fim": f + 15200, "x": 1360, "y": 96, "escala": 0.78})
    ef(f + 700, f"Recibo da viagem: {eur(total)} para 2 ({eur(total / 2)} por pessoa)", "Doc., seção 2: fechamento com o total da viagem (2 pessoas e por pessoa, € e R$). Responde à pergunta do gancho", 14500)
    ev.append({"tipo": "bilhete", "texto": "vale!|leve casaco ✓", "marca": "vale", "x": 1150, "y": 600, "escala": 0.9, "entrada": f + 16200, "saida": f + 22200})
    ef(f + 16200, "Bilhete do veredito: \"vale! leve casaco\" + ✓", "Doc., seção 2: Bilhete com o veredito no fechamento", 6200)
    ev.append({"tipo": "like", "entrada": f + 22700, "saida": f + 26700})
    ef(f + 22700, "Animação \"DEIXA O LIKE E SE INSCREVE\" (2ª vez)", "Doc., seção 2: animação de like e inscrição também no fechamento", 4240)
    ev.append({"tipo": "instagram", "ini": f + 27100, "fim": f + 30800})
    ef(f + 27100, "Chamada SEGUE NO INSTAGRAM (3ª vez)", "Doc., seção 2: 3ª chamada, no fechamento", 3700)
    ev.append({"tipo": "placa", "rotulo": "TODA CIDADE TEM UM", "destino": "PRIMEIRO DIA.", "modulo": "um", "tamanho": "M", "x": 96, "y": 960 - 166, "entrada": f + 31300, "saida": F_fim - 320})
    ev.append({"tipo": "som", "nome": "nascer", "em": f + 31300 + 400, "relDb": -12})
    ef(f + 31300, "Placa de fechamento \"TODA CIDADE TEM UM PRIMEIRO DIA.\" + Nascer do 1º", "DS 4.3 e 5.4: o vídeo termina com a placa de fechamento e o 1º nascendo. Usei a tagline da marca no lugar de \"E ISSO FOI SÓ O PRIMEIRO DIA.\" da amostra, que não serve para um vídeo de 3 dias", F_fim - f - 31300)
    ev.append({"tipo": "telafinal", "ini": F_fim, "proximo": "bruxelas"})
    ef(F_fim, "Transição Página → tela final de 20 s (\"próximo dia: bruxelas →\")", "Doc., seção 2 e amostra aprovada em 16/10/2026", TELA_FINAL)

    # ---------- guia de narração ----------
    if a.guia:
        frases = [{"ini": ini, "fim": fim, "texto": tx} for ini, fim, tx in NARRACAO_GANCHO]
        frases += [{"ini": B_fim + ini, "fim": B_fim + fim, "texto": tx} for ini, fim, tx in NARRACAO_FECHAMENTO]
        ev.append({"tipo": "guia", "inicio": 0, "fim": G, "frases": frases})
        ev.append({"tipo": "guia", "inicio": B_fim, "fim": F_fim, "frases": frases})

    # os sons próprios do vídeo (rufar, fogos) entram na mixagem (rev1/mixar_rev1.py), não no render
    props = {"video": "http://127.0.0.1:8787/proxy1080.mp4", "duracao": duracao, "trechos": trechos, "eventos": [e for e in ev if e["tipo"] != "audio"], "zooms": zooms, "refLufs": REF}
    json.dump(props, open("rev1/props_rev1.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"gancho_ms": G, "corpo_fim_ms": B_fim, "fechamento_fim_ms": F_fim, "duracao_ms": duracao, "audio": audio,
               "narracao_gancho": NARRACAO_GANCHO, "narracao_fechamento": [(B_fim + i, B_fim + j, t) for i, j, t in NARRACAO_FECHAMENTO],
               "sons": [e for e in ev if e["tipo"] == "audio"], "rufar_ms": rufar,
               "dias_ms": [mp.ms(d["corte"]) for d in DIAS[1:]],
               "totais": {"gastos": round(total_gastos, 2), "hotel": round(hotel, 2), "total": round(total, 2), "por_pessoa": round(total / 2, 2), "comida": round(comida, 2)}},
              open("rev1/linha_do_tempo_rev1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def mmss(ms):
        return f"{int(ms // 60000):02d}:{(ms % 60000) / 1000:04.1f}"

    linhas = ["# REV1 · Efeitos visuais e sonoros (vlog de Amsterdam)", "",
              "Gerado por `rev1/montar_rev1.py`. Minutos no **vídeo final** (com gancho e decupagem). Cores dos efeitos: camada de efeitos (decisão do Diego, 21/10/2026); objetos da marca nas cores do DS.", "",
              "| Entra | Dura | Efeito | Por quê |", "|---|---:|---|---|"]
    for e in sorted(efeitos, key=lambda x: x["ms"]):
        d = f"{e['dur'] / 1000:.1f} s" if e["dur"] else ""
        linhas.append(f"| {mmss(e['ms'])} | {d} | {e['nome']} | {e['porque']} |")
    open("rev1/efeitos_rev1.md", "w", encoding="utf-8").write("\n".join(linhas) + "\n")
    print(f"gancho {G / 1000:.2f} s · corpo até {mmss(B_fim)} · fechamento até {mmss(F_fim)} · total {mmss(duracao)}")
    print(f"trechos {len(trechos)} · eventos {len(ev)} · rufar {rufar / 1000:.2f} s")
    print(f"gastos {eur(total_gastos)} · hotel {eur(hotel)} · total {eur(total)} · por pessoa {eur(total / 2)} ({brl(total / 2 * COTACAO)}) · comida {eur(comida)}")


if __name__ == "__main__":
    main()
