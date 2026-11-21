"""Roteiro da REV5 (FINAL) do vlog de Bruges (vídeo longo do YouTube, 16:9, 24 fps): gancho, fechamento, gastos e cotação.

REV5 (Diego, 21/11/2026): "Eu subi no Drive as gravações, o vídeo está aprovado, finalize ele, renderize tudo na maior
qualidade possível. […] Eu tirei a parte dos custos da hospedagem da narração, então tire do vídeo também."
  - As narrações agora são as GRAVADAS (fonte/narracao/P1–P5 = gancho, R1–R8 = fechamento), não o texto do roteiro. Cada
    plano do gancho e do fechamento é reencaixado no que o Diego DISSE: o corte cai na palavra (âncora), e cada take
    continua ≥ 2 s e dentro de um plano da fonte (docs/VIDEO_LONGO_PASSO_A_PASSO.md, item 2).
  - Hotel fora do vídeo: sem a frase F5 (não gravada), sem a linha "Hotel (1 noite)" no Recibo do fechamento e sem hotel
    nas contas. O Recibo final mostra só o que o Diego fala na R4: o que vocês consumiram + o trem = € 132,00 pros dois.
  - Os planos são os da REV4 (aprovada), na mesma ordem de sentido; mudam só os tempos (e o 1º plano do fechamento, que
    passa a ser o canal de tijolo, para o Rozenhoedkaai entrar no "Pois é, ela existe e se chama Bruges").

Fonte: `fonte/1120.mp4` (Drive, Bruges/Youtube, 20/11/2026; 4K HEVC 10 bits, 24 fps, 14:43,5). Tempos da fonte em s.
Valores: foto das anotações do Diego (20/11/2026) + falas do vídeo. Real ↔ euro pela PTAX de venda de 16/03/2026
(segunda-feira, dia do bate-volta), Banco Central: € 1 = R$ 6,0476.
"""

FPS = 24
COTACAO = 6.0476
RODAPE = "cotação € 1 = R$ 6,0476 · PTAX 16/03/2026"
DATA = "16 de março de 2026"
PROXIMO = "paris"  # ordem dos vlogs (CLAUDE.md, pendência 11): Amsterdam, Bruxelas, Bruges, Paris…

# Gastos (fonte em s = quando o gasto é falado ou mostrado na cena do lugar; hora do arquivo no acervo). Iguais à REV4.
GASTOS = [
    {"t": 6.0, "hora": "09:44", "lugar": "TREM BRUXELAS ↔ BRUGES", "cat": "transporte",
     "linhas": [("Ida · 2 × € 18,00", 36.00), ("Volta · 2 × € 18,00", 36.00)],
     "porque": "Anotação do Diego: \"18 euros por trecho por pessoa\"; a tela da máquina (0:05 da fonte) mostra € 72,00. IMG_2417, 09:44, Bruxelas-Central"},
    {"t": 92.5, "hora": "11:27", "lugar": "CHEZ ALBERT", "cat": "comida",
     "linhas": [("2 waffles de chocolate + café", 11.70)],
     "porque": "Anotação \"01:34 – 11,70 euros\"; fala: \"tudo isso aqui deu 11,70, um café e dois waffles de chocolate belga\" (1:32). IMG_2430, 11:27"},
    {"t": 562.2, "hora": "13:57", "lugar": "FRITBAR", "cat": "comida",
     "linhas": [("Batata (prato principal)", 15.00), ("Cerveja + Pepsi", 8.00)],
     "porque": "Anotação \"9:55 – 15 euros da batata – total 23 com as bebidas\"; a fala do pagamento é em 9:22 da fonte (\"a conta deu 23\"). IMG_2611, 13:57"},
    {"t": 576.0, "hora": "14:39", "lugar": "CHEZ ALBERT (2ª VEZ)", "cat": "comida",
     "linhas": [("1 waffle para dividir", 4.70)],
     "porque": "Diego (21/11/2026): \"o waffle foi 4,7\". Fala: \"Gostamos muito e viemos de novo… a gente vai dividir\" (9:35). IMG_2637, 14:39"},
    {"t": 707.0, "hora": "16:10", "lugar": "HOUSE OF WAFFLES", "cat": "comida",
     "linhas": [("Waffle novo", 4.50)],
     "porque": "Anotação \"em algum momento aqui do waffle, você escolhe o melhor momento – 4,50 euros\": no plano do waffle pronto na caixinha (11:47 da fonte), depois que o Bilhete do \"novo waffle\" sai; o letreiro é o da House of Waffles. IMG_2690, 16:10"},
    {"t": 816.0, "hora": "16:18", "lugar": "BAR", "cat": "comida",
     "linhas": [("Cerveja", 5.70)],
     "porque": "Anotação \"13:37 – 5,7 euros cerveja\"; fala: \"bebi a cerveja mais tradicional\" (13:33). IMG_2696, 16:18"},
    {"t": 849.0, "hora": "16:45", "lugar": "CHEZ ALBERT (3ª VEZ)", "cat": "comida",
     "linhas": [("Waffle", 4.70)],
     "porque": "Anotação \"14:12 – mais uma vez chez albert 4,70\"; a Marina: \"só nessa loja a gente já deu dinheiro três vezes\" (14:11). IMG_2699, 16:45"},
    {"t": 869.0, "hora": "16:45", "lugar": "GOFRE · BELGIAN WAFFLES", "cat": "comida",
     "linhas": [("Waffle no palito + caramelo salgado", 5.70)],
     "porque": "Anotação \"14:30 – 5,70 euros – Gofre Belgian Waffles\"; fala: \"waffle num palito belga… topping de caramelo salgado\" (14:16). IMG_2701, 16:45"},
]

# ------------------------------------------------------------------------------------------------
# Narrações gravadas. `arq`: fonte/narracao/<arq>.m4a. `texto`: o que foi dito (Whisper large-v3, conferido em 2 passadas;
# palavras duvidosas em rev5/legenda_duvidas_rev5.md). Posição: `em` (s, relógio do bloco) = onde a FALA começa
# (início medido em dados/narracao_fala.json); `depois` = pausa (s) depois do fim da fala anterior.
NARRACAO_GANCHO = [
    {"id": "G1", "arq": "P1", "em": 0.30, "texto": "Quanto custa um dia em Bruges, a cidade que parece um conto de fadas?"},
    {"id": "G2", "arq": "P2", "depois": 0.30, "texto": "Nós comemos três vezes o mesmo waffle e achamos a melhor batata frita da cidade."},
    # (aqui entra a fala real da Marina: take "Marina", 0,37 s depois do fim da G2)
    {"id": "G3", "arq": "P3", "depois_marina": 0.25, "texto": "E vimos de pertinho o sangue de Cristo."},
    {"id": "G4", "arq": "P4", "depois": 0.35, "texto": "Eu anotei cada euro e eu vou te mostrar no final quanto deu isso tudo e se vale a pena."},
    {"id": "G5", "arq": "P5", "depois": 0.35, "texto": "E a conta começa aqui. Nós saímos de um bate-volta de Bruxelas, cerca de uma hora de Bruxelas, e compramos na hora o bilhete."},
]
MARINA_DEPOIS_G2 = 0.37  # a fala da Marina começa 0,15 s depois do início do take (523,20 da fonte)
FIM_GANCHO_DEPOIS = 0.40  # o gancho (e a música de abertura) acaba 0,4 s depois do fim da G5, no plano do bilhete

# GANCHO: planos da fonte (s), na ordem. `cena`: limites do plano na fonte (cortes de cena de _tmp/cenas.txt, 1 quadro para
# dentro). `ancora`: onde o take começa no relógio do gancho: (narração, palavra, deslocamento s) | número (s) | None (0).
# O fim de cada take é o começo do seguinte; o take sai de `de` e, se não couber até o fim da cena, recua o começo.
# `som`: "fala" (o som do take entra) ou "baixo" (só imagem).
GANCHO = [
    {"de": 344.05, "cena": (343.60, 354.95), "ancora": None, "som": "baixo", "o_que": "Rozenhoedkaai: o canal com a torre do Belfort ao fundo (G1: \"Quanto custa um dia em Bruges\")"},
    {"de": 358.60, "cena": (358.52, 362.14), "ancora": 3.00, "som": "baixo", "o_que": "canal com a torre da igreja e um barco (G1: \"um conto de fadas\")"},
    {"de": 84.45, "cena": (84.44, 86.77), "ancora": ("G2", "vezes", -0.10), "som": "baixo", "o_que": "waffle do Chez Albert com a bandeirinha da Bélgica (G2: \"três vezes o mesmo waffle\")"},
    {"de": 506.75, "cena": (506.73, 509.27), "ancora": ("G2", "batata", -0.20), "som": "baixo", "o_que": "a batata do Fritbar (G2: \"a melhor batata frita da cidade\")"},
    {"de": 523.05, "cena": (516.30, 574.10), "ancora": "marina", "som": "fala", "o_que": "Marina: \"Um dos pratos mais saborosos que eu já comi. E foi só uma batata frita, tá?\"", "dur_fixa": 5.40},
    {"de": 284.35, "cena": (284.35, 288.27), "ancora": "fim_marina", "som": "baixo", "o_que": "fachada dourada da Basílica do Sangue Sagrado (G3: \"o sangue de Cristo\")"},
    {"de": 292.00, "cena": (291.81, 294.98), "ancora": ("G4", "euro", 0.30), "som": "baixo", "o_que": "canal com as bandeiras e os barcos (G4: \"no final quanto deu\")"},
    {"de": 295.05, "cena": (295.02, 298.64), "ancora": ("G4", "isso", -0.10), "som": "baixo", "o_que": "canal entre casas de tijolo (G4: \"e se vale a pena\")"},
    {"de": 3.80, "cena": (0.0, 9.30), "ancora": ("G5", "aqui", -0.12), "som": "baixo", "o_que": "compra do bilhete na máquina da Bruxelas-Central: resumo com € 72,00 e pagamento (G5: \"E a conta começa aqui\")"},
]
# A tela do bilhete (REV4: 4,5 s) passa a 5,5 s: a G5 gravada explica a compra ("…e compramos na hora o bilhete"). De 3,80 a
# 9,26 da fonte: o resumo com € 72,00 e o pagamento; depois de 9,3 s a câmera vira (movimento 3× maior).

# Primeira cena depois do gancho (placa 1 DIA EM BRUGES →): a chegada na estação de Bruges
CHEGADA = (10.10, 20.05)  # "Acabamos de chegar aqui em Bruges, e aí a gente vai passar o dia aqui…"

# ------------------------------------------------------------------------------------------------
# FECHAMENTO: entra depois do "não tem um defeito, venham demais." do Diego (14:42,3 da fonte). Relógio do fechamento:
# 0 = fim do corpo. Nenhum plano repete o do gancho.
FIM_CORPO = 882.55
NARRACAO_FECHAMENTO = [
    {"id": "F1", "arq": "R1", "em": 0.65, "texto": "Sabe aquela Europa que você imagina antes de visitar a Europa? Pois é, ela existe e se chama Bruges."},
    {"id": "F2", "arq": "R2", "depois": 0.40, "texto": "Conhecida como Veneza do Norte, ela tem um canal em cada esquina, carruagens passando, cheira a chocolate e a waffle."},
    {"id": "F3", "arq": "R3", "depois": 0.55, "texto": "O centro histórico inteiro é patrimônio mundial da UNESCO e dá pra fazer tudo andando."},
    {"id": "F4", "arq": "R4", "depois": 0.45, "texto": "No final das contas, tudo que nós consumimos aqui, mais o transporte saindo de Bruxelas, ficou 132 euros para o casal."},
    {"id": "F6", "arq": "R5", "depois": 0.45, "texto": "Vale muito a pena visitar essa cidade. Um dia é o suficiente para você conhecer, mas não para querer ir embora. Eu voltaria mil vezes."},
    {"id": "F7", "arq": "R6", "depois": 0.45, "texto": "E a dica que eu dou é: durma na cidade. De manhã cedo e à noite, os bate-voltas vão embora e ela fica mais vazia e mais legal ainda de conhecer."},
    {"id": "F8", "arq": "R7", "depois": 0.45, "texto": "E se esse vídeo te ajudou de alguma forma, se inscreve e deixa o like aí, que vai me ajudar muito. E não se esquece de me seguir lá no Instagram, @primeirodiaem."},
    {"id": "F9", "arq": "R8", "depois": 0.45, "texto": "Toda cidade tem um primeiro dia, e o de Bruges a gente nunca vai esquecer. O próximo é em Paris, te espero lá."},
]
FECHAMENTO = [
    {"de": 461.55, "cena": (461.52, 465.02), "ancora": None, "o_que": "casas de tijolo sobre o canal (F1: \"Sabe aquela Europa que você imagina…\")"},
    {"de": 349.60, "cena": (348.60, 354.95), "ancora": 3.48, "o_que": "Rozenhoedkaai aberto (F1: \"Pois é, ela existe e se chama Bruges\")"},
    {"de": 458.45, "cena": (458.40, 461.48), "ancora": ("F2", "norte", -0.19), "o_que": "canal com o salgueiro (F2: \"um canal em cada esquina\")"},
    {"de": 217.05, "cena": (217.02, 219.81), "ancora": ("F2", "carruagens", -0.09), "o_que": "carruagens no Markt (F2: \"carruagens passando\")"},
    {"de": 468.10, "cena": (468.06, 471.31), "ancora": ("F2", "chocolate", 0.01), "o_que": "vitrine de chocolate (F2: \"cheira a chocolate e a waffle\")"},
    {"de": 151.00, "cena": (150.52, 154.64), "ancora": ("F2", "chocolate", 2.01), "o_que": "Markt: a torre do Belfort (F3: \"patrimônio mundial da UNESCO\")"},
    {"de": 278.45, "cena": (278.40, 284.31), "ancora": ("F3", "dá", -0.12), "o_que": "Marina andando no Burg (F3: \"dá pra fazer tudo andando\")"},
    {"de": 220.00, "cena": (219.85, 224.14), "ancora": ("F4", "tudo", -0.12), "o_que": "Markt: as fachadas coloridas (F4: \"tudo que nós consumimos\", Recibo)"},
    {"de": 272.10, "cena": (272.02, 275.27), "ancora": ("F4", "ficou", -0.12), "o_que": "Burg: a prefeitura gótica (F4: \"ficou 132 euros para o casal\")"},
    {"de": 618.20, "cena": (618.15, 621.98), "ancora": ("F6", "ini", -0.10), "o_que": "carruagem passando no Begijnhof (F6: \"Vale muito a pena\")"},
    {"de": 683.25, "cena": (683.23, 686.81), "ancora": ("F6", "mas", -0.10), "o_que": "Minnewater: o lago e o castelinho (F6: \"Eu voltaria mil vezes\")"},
    {"de": 62.10, "cena": (62.06, 65.27), "ancora": ("F7", "ini", -0.10), "o_que": "rua tranquila de manhã, quase sem gente (F7: \"durma na cidade\")"},
    {"de": 65.35, "cena": (65.31, 68.27), "ancora": ("F7", "bate", 0.06), "o_que": "a Marina sozinha numa ruela vazia (F7: \"ela fica mais vazia\")"},
    {"de": 693.35, "cena": (693.31, 696.69), "ancora": ("F7", "bate", 3.02), "o_que": "Minnewater com a torre ao fundo (F8: \"se esse vídeo te ajudou\")"},
    {"de": 689.75, "cena": (689.73, 693.27), "ancora": ("F8", "muito", -0.93), "o_que": "Marina andando na beira do Minnewater (F8: Instagram)"},
    {"de": 227.15, "cena": (227.14, 233.23), "ancora": ("F8", "arroba", -0.10), "o_que": "Markt: bandeiras, estátua e o Belfort (F9: \"Toda cidade tem um primeiro dia\")"},
    {"de": 686.90, "cena": (686.88, 689.10), "ancora": ("F9", "paris", -0.10), "o_que": "vocês dois acenando (F9: \"O próximo é em Paris, te espero lá\"); termina antes da câmera girar (689,15)", "dur_fixa": 2.20},
]


def contas():
    """Gastos do dia (comida + trem), pros dois e por pessoa. REV5: sem hotel (pedido do Diego, 21/11/2026)."""
    cat = {"comida": 0.0, "transporte": 0.0}
    for g in GASTOS:
        for _, v in g["linhas"]:
            cat[g["cat"]] += v
    total = cat["comida"] + cat["transporte"]
    return {"comida": round(cat["comida"], 2), "transporte": round(cat["transporte"], 2), "total": round(total, 2),
            "pp": round(total / 2, 2), "pp_brl": round(total / 2 * COTACAO, 2)}
