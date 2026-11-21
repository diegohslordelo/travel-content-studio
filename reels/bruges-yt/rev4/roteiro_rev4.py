"""Roteiro da REV4 do vlog de Bruges (vídeo longo do YouTube, 16:9, 24 fps): gancho, fechamento, gastos e cotação.

REV2 (pedidos do Diego, 21/11/2026): mais canal no gancho; fechamento com frases mais fortes, além dos custos ("Bruges é
o que você imagina da Europa antes de ir pra lá", melhorada); a 2ª ida ao Chez Albert foi € 4,70; a relíquia fica
exposta das 14h às 16h. O `keen` sai (mixagem). REV3: só a música muda. REV4 (Diego, 21/11/2026): a dica do fim
muda ("fale pra galera dormir um dia na cidade pra aproveitar Bruges mais vazia") e o último take termina antes da câmera girar.

Dados de um lugar só, lidos por `rev4/previas_narracao_rev4.py` (prévias do gancho e do fechamento com contador, para o
Diego gravar) e, depois, pelo `montar` do vídeo inteiro.

Fonte: `fonte/1120.mp4` (Drive, Bruges/Youtube, 20/11/2026; 4K HEVC 10 bits, 24 fps, 14:43,5). Tempos da fonte em s.
Valores: foto das anotações do Diego (20/11/2026) + falas do vídeo. Real ↔ euro pela PTAX de venda de 16/03/2026
(segunda-feira, dia do bate-volta), Banco Central: € 1 = R$ 6,0476.
"""

FPS = 24
COTACAO = 6.0476
RODAPE = "cotação € 1 = R$ 6,0476 · PTAX 16/03/2026"
DATA = "16 de março de 2026"
HOTEL_BRL_2_NOITES = 1738.78  # ibis Brussels off Grand Place, 2 noites, 2 pessoas (Diego, 06/11/2026, vlog de Bruxelas)
NOITES_NO_DIA = 1  # Bruxelas levou 1 das 2 noites; a outra é a do bate-volta (narração H1 de Bruxelas). A confirmar
PROXIMO = "paris"  # ordem dos vlogs (CLAUDE.md, pendência 11): Amsterdam, Bruxelas, Bruges, Paris…

# Gastos (fonte em s = quando o gasto é falado ou mostrado na cena do lugar; hora do arquivo no acervo).
# `valor` None = falta o valor (fica fora das contas até o Diego mandar).
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
# GANCHO: planos da fonte (s), na ordem. `som`: "fala" (o som do take entra) ou "baixo" (imagem; som da fonte mudo:
# nesses planos o Diego deixou o áudio em silêncio digital). Todo take ≥ 2 s e dentro de um plano (cortes de cena
# em _tmp/cenas.txt). O último é a compra do bilhete (pedido do Diego: ~4 s, fecha a música de abertura).
GANCHO = [
    # REV2 (Diego: "quero mais vídeo do canal no gancho"): 4 planos de canal (eram 1); saem as carruagens e o Belfort,
    # que vão para o fechamento
    {"de": 344.05, "ate": 347.45, "o_que": "Rozenhoedkaai: o canal com a torre do Belfort ao fundo (o cartão-postal de Bruges)", "som": "baixo"},
    {"de": 358.60, "ate": 361.95, "o_que": "canal com a torre da igreja ao fundo e um barco", "som": "baixo"},
    {"de": 84.45, "ate": 86.70, "o_que": "waffle do Chez Albert com a bandeirinha da Bélgica (close)", "som": "baixo"},
    {"de": 506.75, "ate": 509.20, "o_que": "a batata do Fritbar (close do prato)", "som": "baixo"},
    {"de": 523.05, "ate": 528.45, "o_que": "Marina: \"Um dos pratos mais saborosos que eu já comi. E foi só uma batata frita, tá?\"", "som": "fala"},
    {"de": 284.35, "ate": 288.27, "o_que": "fachada dourada da Basílica do Sangue Sagrado, no Burg", "som": "baixo"},
    {"de": 292.00, "ate": 294.90, "o_que": "canal com as bandeiras e os barcos", "som": "baixo"},
    {"de": 295.05, "ate": 297.80, "o_que": "canal entre casas de tijolo", "som": "baixo"},
    {"de": 4.70, "ate": 9.20, "o_que": "compra do bilhete de trem na máquina da Bruxelas-Central (tela de pagamento: € 72,00)", "som": "baixo"},
]
# Narração do gancho (a gravar; o texto é o da REV1): onde começa no relógio do gancho (ms) e duração estimada
# (≈ 3,2 palavras/s + 0,3 s, o ritmo das narrações de Bruxelas). Depois da gravação, o encaixe é refeito pelo que foi DITO.
NARRACAO_GANCHO = [
    {"id": "G1", "em": 200, "texto": "Quanto custa um dia em Bruges, a cidade que parece um conto de fadas?"},
    {"id": "G2", "em": 5100, "texto": "Voltamos três vezes no mesmo waffle e achamos a melhor batata da viagem."},
    {"id": "G3", "em": 17100, "texto": "E vimos de pertinho a relíquia do sangue de Cristo."},
    {"id": "G4", "em": 20750, "texto": "Eu anotei cada euro. No final, te mostro quanto deu e se vale a pena."},
    {"id": "G5", "em": 25950, "texto": "E a conta começa aqui, ainda em Bruxelas."},
]

# Primeira cena depois do gancho (a "vinheta": placa 1 DIA EM BRUGES →): a chegada na estação de Bruges
CHEGADA = (10.10, 20.05)  # "Acabamos de chegar aqui em Bruges, e aí a gente vai passar o dia aqui…"

# ------------------------------------------------------------------------------------------------
# FECHAMENTO: entra depois do "não tem um defeito, venham demais." do Diego (14:42,3 da fonte), sobre as melhores
# paisagens do dia (o vídeo termina numa selfie). Nenhum plano repete o do gancho.
FIM_CORPO = 882.55
FECHAMENTO = [
    # REV2: planos na ordem das frases novas (nenhum repete o gancho); entre parênteses, a frase em que o plano cai
    {"de": 349.60, "ate": 354.90, "o_que": "Rozenhoedkaai aberto (F1: \"a Europa que você imagina\")"},
    {"de": 461.55, "ate": 465.00, "o_que": "casas de tijolo sobre o canal (F2: \"canal em cada esquina\")"},
    {"de": 217.05, "ate": 219.75, "o_que": "carruagens no Markt (F2: \"carruagem passando na praça\")"},
    {"de": 468.10, "ate": 471.25, "o_que": "vitrine de chocolate (F2: \"cheiro de chocolate e waffle\")"},
    {"de": 151.00, "ate": 153.60, "o_que": "Markt: a torre do Belfort (F3: \"Patrimônio Mundial da UNESCO\")"},
    {"de": 278.45, "ate": 284.25, "o_que": "Marina andando no Burg (F3: \"dá pra conhecer tudo a pé\")"},
    {"de": 458.45, "ate": 461.40, "o_que": "canal com o salgueiro (F4: os custos)"},
    {"de": 220.00, "ate": 223.95, "o_que": "Markt: as fachadas coloridas (F5: o total)"},
    {"de": 272.10, "ate": 275.20, "o_que": "Burg: a prefeitura gótica"},
    {"de": 618.20, "ate": 621.90, "o_que": "carruagem passando no Begijnhof (F6: o veredito)"},
    {"de": 62.10, "ate": 65.20, "o_que": "rua tranquila de manhã, quase sem gente (F7: a dica de dormir na cidade)"},
    {"de": 65.35, "ate": 68.25, "o_que": "a Marina sozinha numa ruela vazia (F7: \"a cidade fica bem mais vazia\")"},
    {"de": 683.25, "ate": 686.75, "o_que": "Minnewater: o lago e o castelinho"},
    {"de": 693.35, "ate": 696.65, "o_que": "Minnewater com a torre ao fundo (F8: like e Instagram)"},
    {"de": 689.75, "ate": 693.25, "o_que": "Marina andando na beira do Minnewater"},
    {"de": 227.15, "ate": 233.20, "o_que": "Markt: bandeiras, estátua e o Belfort (F9: \"Toda cidade tem um primeiro dia\")"},
    {"de": 686.90, "ate": 689.10, "o_que": "vocês dois acenando para a câmera (no \"Te espero lá!\"); termina antes da câmera girar (689,15)"},
]
# `em` None: começa 0,35 s depois do fim estimado do bloco anterior
NARRACAO_FECHAMENTO = [
    {"id": "F1", "em": 900, "texto": "Sabe aquela Europa que você imagina antes de conhecer a Europa? Ela existe. E se chama Bruges."},
    {"id": "F2", "em": None, "texto": "Canal em cada esquina, carruagem passando na praça e uma cidade inteira com cheiro de chocolate e waffle."},
    {"id": "F3", "em": None, "texto": "O centro histórico inteiro é Patrimônio Mundial da UNESCO, e dá pra conhecer tudo a pé."},
    {"id": "F4", "em": None, "texto": "E tudo isso num bate-volta: trem, waffle, batata e cerveja deram {gastos} euros pra nós dois."},
    {"id": "F5", "em": None, "texto": "Somando a noite de hotel, ficou em uns {total} euros: {pp} por pessoa, perto de {pp_brl} reais."},
    {"id": "F6", "em": None, "texto": "Vale a pena? Muito. Um dia é suficiente pra conhecer, mas não pra querer ir embora. Eu voltaria mil vezes."},
    {"id": "F7", "em": None, "texto": "Dica: se puder, durma uma noite em Bruges. De manhã cedo e à noite, quando os grupos de bate-volta vão embora, a cidade fica bem mais vazia."},
    {"id": "F8", "em": None, "texto": "Se esse vídeo te ajudou, se inscreve, deixa o like e me segue no Instagram: arroba primeirodiaem."},
    {"id": "F9", "em": None, "texto": "Toda cidade tem um primeiro dia. E o de Bruges, a gente nunca vai esquecer. O próximo é em Paris. Te espero lá!"},
]


def dur_estimada(texto):
    """Duração estimada da fala (s): ≈ 3,2 palavras/s + 0,3 s (ritmo das narrações gravadas de Bruxelas)."""
    return len(texto.split()) / 3.2 + 0.3


def contas(valor_ca2=None):
    """Gastos do dia, hotel (1 noite) e total. `valor_ca2`: valor da 2ª ida ao Chez Albert (None = fora da conta)."""
    gastos = 0.0
    for g in GASTOS:
        for _, v in g["linhas"]:
            if v is None:
                v = valor_ca2 or 0.0
            gastos += v
    hotel = HOTEL_BRL_2_NOITES / 2 * NOITES_NO_DIA / COTACAO
    total = gastos + hotel
    pp = total / 2
    return {"gastos": round(gastos, 2), "hotel": round(hotel, 2), "total": round(total, 2), "pp": round(pp, 2), "pp_brl": round(pp * COTACAO, 2)}
