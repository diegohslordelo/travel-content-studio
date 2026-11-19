"""Montagem da REV1 do Reel BXL-decepção (Bruxelas × Bruges), narrado sobre o acervo.

Roda de reels/bxl-decepcao (depois de `python3 rev1/decupar_voz.py`):
    python3 rev1/montar_rev1.py            props + legendas + efeitos + extração dos planos
    python3 rev1/montar_rev1.py --sem-clipes   só props/legendas/efeitos (planos já extraídos)

Entrada
  rev1/voz_rev1.json                       palavras com o tempo no Reel (decupagem)
  fonte/clipes/*.MOV                       planos do acervo baixados do Drive (fora do git)
  rev1/mapa/belgica_naturalearth_50m.json  contorno da Bélgica (Natural Earth 1:50m, domínio público)

Saída
  public/clipes/sNN_*.mp4                  cada plano já recortado no tamanho da tela (SDR BT.709, 24 qps, mudo)
  rev1/props_rev1.json                     props da composição `ReelFormato` (Remotion)
  rev1/efeitos_rev1.json                   efeitos sonoros e trilha para a mixagem (`rev1/mixar_rev1.py`)
  rev1/roteiro_de_cortes_rev1.md           tabela cena a cena: tempo, fala, imagem, transição e som

Regras usadas
  - cada troca de imagem cai 0,08 s antes da palavra que ela mostra (FORMATOS_REELS 7.1);
  - nenhum take esticado: o trecho usado cabe no take (FORMATOS_REELS 8.3);
  - texto na tela só com palavra dita na fala (decisão do Diego); a placa do CTA é o único elemento do DS;
  - DS só no CTA (decisão do Diego, 28/10/2026): o resto usa a linguagem do formato (Anton, Inter, âmbar).
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor

FPS = 24
ANTES = 0.08
TM = ("zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

voz = json.load(open("rev1/voz_rev1.json"))
PAL = voz["palavras"]
DUR_VOZ = voz["duracao"]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def W(palavra, depois=0.0):
    """Início (s) da 1ª ocorrência da palavra a partir de `depois`."""
    alvo = norm(palavra)
    for p in PAL:
        if p["s"] >= depois - 1e-6 and norm(p["w"]) == alvo:
            return p["s"]
    sys.exit(f"palavra não encontrada: {palavra} (depois de {depois})")


def corte(t):
    """Tempo de corte em quadros: 0,08 s antes da palavra."""
    return max(0, round((t - ANTES) * FPS))


def q(t):
    return round(t * FPS)


# ------------------------------------------------------------------------------------------------
# Cenas. ini = palavra que a imagem mostra. Cada plano: arquivo, entrada no take (s), foco x (0–1) e
# pan opcional (foco final), tamanho da camada (full 1080×1920, meia 1080×960, grade 540×960).
# Cidade: "bxl" (grade mais fria e contida) ou "bru" (grade quente, saturada): a evolução visual pedida.
# ------------------------------------------------------------------------------------------------
t_e1 = W("e", 2.0)            # "e agora entendi…"
t_entendi = W("entendi")
t_tem9 = W("tem", 9.0)
t_famosa = W("famosa")
t_conhecer = W("conhecer")
t_foi_em = W("foi", 6.5)
t_nos = W("Nós")
t_bru = W("Bruxelas", 7.0)
t_e_vou = W("e", t_bru)       # "e eu vou te falar"
t_comida = W("comida")
t_lugares = W("lugares")
t_mas = W("mas", 11.0)
t_falta1 = W("falta", 12.0)
t_coisa1 = W("coisa", 12.0)
t_para = W("Para")
t_manneken = W("Manneken")
t_ja = W("já", 17.0)
t_considerado = W("considerado")
t_decep = W("decepcionantes")
t_mas2 = W("Mas", 20.0)
t_monte = W("Monte")
t_tem = W("tem", 26.0)
t_cervejas = W("cervejas")
t_so = W("Só")
t_bahia = W("Bahia")
t_foi = W("foi", 34.0)
t_ate = W("Até")
t_fomos = W("fomos")
t_bruges1 = W("Bruges", 38.0)
t_e_ai = W("e", 39.4)
t_exatamente = W("exatamente", 42.0)
t_que_voce = W("que", 44.3)
t_ruazinhas = W("Ruazinhas")
t_canais = W("canais")
t_casinhas = W("casinhas")
t_construcoes = W("construções")
t_a_cidade = W("a", 50.5)
t_sensacao = W("sensação", 52.0)
t_literalmente = W("literalmente")
t_nao = W("Não", 55.0)
t_tempero = W("tempero")
t_bruges2 = W("Bruges", 59.0)
t_se = W("Se", 62.0)
t_so2 = W("só", 64.0)
t_se2 = W("se", 66.5)
t_la = W("lá", 68.5)
FIM_VOZ = PAL[-1]["e"]

CTA_INI = round(FIM_VOZ + 0.05, 2)   # a placa chega quando a última palavra termina
CTA_DUR = 2.6
DUR_TOTAL = CTA_INI + CTA_DUR

# virada: a fala "É exatamente isso que estava faltando" (o "É" fica 0,1 s antes de "exatamente")
t_virada = t_exatamente - 0.12

CENAS = [
    # id, ini (s), tipo, cidade, planos, extras
    dict(id="s01_gancho", ini=0.0, cidade="bxl", planos=[dict(arq="IMG_2211.MOV", entrada=0.0, foco=0.47, foco2=0.53)],
         zoom=[1.0, 1.06], fala="Visitei a cidade mais superestimada da Europa",
         imagem="Marina entrando na Grand-Place (dia), câmera andando atrás dela", transicao="—", som="voz + trilha (Investigations) entra seca"),
    dict(id="s02_tanta_gente", ini=t_entendi, cidade="bxl", planos=[dict(arq="IMG_2212.MOV", entrada=0.4, foco=0.55)],
         zoom=[1.04, 1.0], fala="e agora entendi por que tanta gente se decepciona.",
         imagem="Grand-Place cheia de turistas", transicao="corte seco", som="—"),
    dict(id="s03_mapa_belgica", ini=t_nos, tipo="mapa", modo="belgica", cidade="bxl",
         fala="Nós passamos dois dias na Bélgica e um deles foi em",
         imagem="Animação: contorno da Bélgica; BÉLGICA na palavra; ponto e rótulo de BRUXELAS em \"foi em\" (a imagem da cidade entra em \"Bruxelas\")", transicao="corte seco", som="—"),
    dict(id="s04_grand_place", ini=t_bru, cidade="bxl", planos=[dict(arq="IMG_2190.MOV", entrada=1.0, foco=0.42, foco2=0.62)],
         zoom=[1.0, 1.03], fala="Bruxelas, e eu vou te falar, é uma cidade bonita,",
         imagem="Panorâmica da Grand-Place (Maison du Roi)", transicao="corte seco", som="—"),
    dict(id="s05_comida_lugares", ini=t_tem9, tipo="split", cidade="bxl",
         planos=[dict(arq="IMG_2205.MOV", entrada=0.4, foco=0.5, entra=t_tem9),
                 dict(arq="IMG_2241.MOV", entrada=0.6, foco=0.5, entra=t_lugares)],
         fala="tem comida boa, lugares interessantes,",
         imagem="Tela dividida: sanduíche de batata frita (Fritland) em cima; Galeria Saint-Hubert entra embaixo em \"lugares\"", transicao="painel de baixo entra deslizando", som="—"),
    dict(id="s06_falta", ini=t_mas, cidade="bxl", planos=[dict(arq="IMG_2397.MOV", entrada=1.6, foco=0.55)],
         zoom=[1.0, 1.05], desat=[t_falta1, t_coisa1 + 0.45, 0.22], fala="mas parece que falta alguma coisa. Para você ter ideia, a atração mais",
         imagem="Boulevard Anspach ao entardecer; a cor escorre em \"falta alguma coisa\"", transicao="corte seco", som="—"),
    dict(id="s07_atracao", ini=t_famosa, cidade="bxl", planos=[dict(arq="IMG_2255.MOV", entrada=0.2, foco=0.47, foco2=0.37)],
         zoom_kf=[(t_famosa, 1.0), (t_manneken - 0.05, 1.04), (t_manneken + 0.55, 1.5), (t_ja, 1.56)], origem="50% 44%",
         fala="famosa da cidade, o Manneken Pis, do menino fazendo xixi,",
         imagem="Multidão de celular na mão; em \"Manneken\" a câmera fecha no menino minúsculo no nicho (escala vira a piada)",
         transicao="corte seco + aproximação no mesmo plano", som="—"),
    dict(id="s08_noticia", ini=t_ja, cidade="bxl", planos=[dict(arq="IMG_2251.MOV", entrada=0.0, foco=0.5)],
         zoom=[1.1, 1.18], origem="50% 40%", fala="já foi considerado um dos pontos turísticos mais decepcionantes da Europa.",
         imagem="Recorte da notícia real (VRT NWS, 04/12/2012) sobre o Manneken Pis desfocado (vertical nativo); marca-texto em \"most disappointing\"",
         transicao="recorte cai como papel", som="página (−8 dB) na entrada; chicote leve (−10 dB) no marca-texto"),
    dict(id="s10_grand_place_noite", ini=t_mas2, cidade="bxl", planos=[dict(arq="IMG_2411.MOV", entrada=0.0, foco=0.36, foco2=0.5)],
         zoom=[1.0, 1.04], grade_quente=True, entrada="dissolve", fala="Mas também não posso ser injusto, a cidade também tem sua beleza, a Grand Place é linda,",
         imagem="Marina entrando na Grand-Place à noite", transicao="o recorte sai para baixo e revela a praça (dissolve 0,3 s)", som="—"),
    dict(id="s11_mont_des_arts", ini=t_monte, cidade="bxl", planos=[dict(arq="IMG_2365.MOV", entrada=1.2, foco=0.66, foco2=0.7)],
         zoom=[1.0, 1.04], grade_quente=True, fala="o Monte das Artes no final de tarde é maravilhoso,",
         imagem="Jardim do Mont des Arts com a torre da prefeitura ao fundo (17h22)", transicao="corte seco", som="—"),
    dict(id="s12_waffle_cerveja", ini=t_tem, tipo="split", cidade="bxl", grade_quente=True,
         planos=[dict(arq="IMG_2232.MOV", entrada=0.0, foco=0.6, entra=t_tem),
                 dict(arq="AC2A8D11.mp4", entrada=0.0, foco=0.5, entra=t_cervejas)],
         fala="tem waffles muito gostosos e cervejas muito boas.",
         imagem="Tela dividida: Marina mordendo o waffle com chocolate em cima; Hoegaarden entra embaixo em \"cervejas\"", transicao="painel de baixo entra deslizando", som="—"),
    dict(id="s13_so_que", ini=t_so, cidade="bxl", planos=[dict(arq="IMG_2181.MOV", entrada=0.3, foco=0.5)],
         zoom=[1.0, 1.04], desat=[t_so, t_so + 1.0, 0.3], fala="Só que falta alguma coisa,",
         imagem="Avenida larga e sem graça (Heysel); a cor sai", transicao="corte seco", som="—"),
    dict(id="s14_sem_sal", ini=t_bahia, cidade="bxl", planos=[dict(arq="IMG_2369.MOV", entrada=0.5, foco=0.45)],
         zoom=[1.0, 1.05], brilho=0.8, desat=[t_bahia, t_bahia + 0.1, 0.3], fala="aqui na Bahia a gente falaria que falta um molho, tá sem sal,",
         imagem="Céu branco, bandeiras e prédio cinza (Bruxelas)", transicao="corte seco", som="—"),
    dict(id="s15_sensacao", ini=t_foi, cidade="bxl", planos=[dict(arq="IMG_2381.MOV", entrada=9.4, foco=0.52)],
         zoom=[1.0, 1.03], desat=[t_foi, t_foi + 0.1, 0.55], fala="foi exatamente essa a sensação que eu tive.",
         imagem="Diego tomando cerveja no bar em Bruxelas, sem falar (trecho em que ele bebe)", transicao="corte seco", som="trilha de Bruxelas sai no fim da frase"),
    dict(id="s16_trem", ini=t_ate, cidade="bxl", planos=[dict(arq="IMG_2417.MOV", entrada=0.6, foco=0.58)],
         zoom=[1.0, 1.06], fala="Até que no dia seguinte nós pegamos um trem e fomos",
         imagem="Máquina de passagens de trem (estação, 16/03 09h44)", transicao="corte seco", som="Reunited entra por baixo"),
    dict(id="s17_mapa_trem", ini=t_conhecer, tipo="mapa", modo="trem", cidade="bru",
         fala="conhecer Bruges,",
         imagem="Animação: linha do trem de Bruxelas a Bruges; BRUGES na palavra", transicao="corte seco", som="chicote (−6 dB) quando a linha corre"),
    dict(id="s18_chegada", ini=t_e_ai, cidade="bru", planos=[dict(arq="IMG_2426.MOV", entrada=0.3, foco=0.5)],
         zoom=[1.0, 1.05], fala="e aí a Bélgica finalmente mostrou sua cara.",
         imagem="Primeira rua de Bruges: tijolo, pedra e o Belfort lá no fundo", transicao="corte seco", som="riser (−8 dB) sobe até a virada"),
    dict(id="s19_virada", ini=t_virada, cidade="bru", planos=[dict(arq="IMG_2492.MOV", entrada=0.3, foco=0.36, foco2=0.56)],
         zoom=[1.08, 1.0], luz=True, fala="É exatamente isso que estava faltando,",
         imagem="Rozenhoedkaai: canal, Belfort e barco passando (a melhor imagem guardada para a virada)",
         transicao="LUZ DE PASSAGEM: luz quente desce e esconde o corte", som="ar longo (−6 dB) no pico da luz; Reunited abre (aos 37,5 s da faixa)"),
    dict(id="s20_europa_imagina", ini=t_que_voce, cidade="bru", planos=[dict(arq="IMG_2672.MOV", entrada=3.0, foco=0.5)],
         zoom=[1.0, 1.04], fala="sabe aquela Europa que você imagina antes de ir para a Europa?",
         imagem="Lago Minnewater (vertical nativo), panorâmica até a torre", transicao="corte seco", som="—"),
    dict(id="s21_lista", ini=t_ruazinhas, tipo="grade", cidade="bru",
         planos=[dict(arq="IMG_2427.MOV", entrada=0.3, foco=0.5, entra=t_ruazinhas),
                 dict(arq="IMG_2486.MOV", entrada=1.6, foco=0.42, entra=t_canais),
                 dict(arq="IMG_2448.MOV", entrada=0.8, foco=0.52, entra=t_casinhas),
                 dict(arq="IMG_2479.MOV", entrada=0.4, foco=0.5, entra=t_construcoes)],
         fala="Ruazinhas de pedra, canais, casinhas medievais, construções maravilhosas",
         imagem="Grade 2×2, cada quadro entra na palavra: Marina na ruela de pedra · canal com barco · casas do Markt · Basílica do Sangue Sagrado",
         transicao="quadros entram um a um", som="—"),
    dict(id="s22_chocolate", ini=t_a_cidade, cidade="bru", planos=[dict(arq="IMG_2603.MOV", entrada=0.2, foco=0.5)],
         zoom=[1.0, 1.06], fala="e a cidade ainda cheira a chocolate.",
         imagem="Vitrine de chocolates em Bruges", transicao="corte seco", som="—"),
    dict(id="s23_filme", ini=t_sensacao, cidade="bru", planos=[dict(arq="IMG_2644.MOV", entrada=0.0, foco=0.38, foco2=0.55)],
         zoom=[1.0, 1.03], cinema=t_literalmente, fala="A sensação de que você está literalmente dentro de um filme.",
         imagem="Carruagem passando em frente às casas de tijolo; faixas de cinema entram em \"literalmente\"", transicao="corte seco", som="—"),
    dict(id="s24_comparar", ini=t_nao, tipo="comparar", cidade="bxl",
         planos=[dict(arq="IMG_2216.MOV", entrada=0.3, foco=0.55, cidade="bxl"),
                 dict(arq="IMG_2183.MOV", entrada=0.2, foco=0.4, cidade="bxl", entra=t_bruges2, rotulo="BRUXELAS"),
                 dict(arq="IMG_2577.MOV", entrada=0.4, foco=0.35, cidade="bru", entra=t_bruges2, rotulo="BRUGES")],
         desat=[t_tempero, t_tempero + 0.6, 0.35],
         fala="Não é que foi ruim estar em Bruxelas, mas enquanto falta aquele tempero na cidade, Bruges entrega tudo que você sempre imaginou sobre a Bélgica.",
         imagem="Grand-Place de dia (perde a cor em \"tempero\"); em \"Bruges\" a tela divide: Bruxelas sem cor em cima, canal de Bruges vivo embaixo",
         transicao="tela divide em \"Bruges\"", som="chicote (−6 dB) na divisão"),
    dict(id="s25_marina", ini=t_se, cidade="bru", planos=[dict(arq="IMG_2594.MOV", entrada=2.0, foco=0.5)],
         zoom=[1.0, 1.04], fala="Se você tá planejando conhecer a Bélgica, não fique",
         imagem="Marina caminhando na alameda de Bruges, torre ao fundo", transicao="corte seco", som="—"),
    dict(id="s26_barco", ini=t_so2, cidade="bru", planos=[dict(arq="IMG_2591.MOV", entrada=1.8, foco=0.55)],
         zoom=[1.0, 1.04], fala="só em Bruxelas, reserve esse dia pra Bruges e",
         imagem="Barco de turistas passando no canal", transicao="corte seco", som="—"),
    dict(id="s27_minnewater", ini=t_se2, cidade="bru", planos=[dict(arq="IMG_2651.MOV", entrada=2.6, foco=0.62)],
         zoom=[1.0, 1.04], fala="se puder durma na cidade, porque foi",
         imagem="Lago Minnewater e o castelinho", transicao="corte seco", som="—"),
    dict(id="s28_nos", ini=t_la, cidade="bru", planos=[dict(arq="IMG_2654.MOV", entrada=1.5, foco=0.6)],
         zoom=[1.0, 1.02], fala="lá que eu encontrei a Europa que eu tava procurando.",
         imagem="Diego e Marina acenando em Bruges (selfie)", transicao="corte seco", som="—"),
    dict(id="s29_cta", ini=CTA_INI - 0.1, cidade="bru", planos=[dict(arq="IMG_2491.MOV", entrada=0.3, foco=0.42, foco2=0.5)],
         zoom=[1.0, 1.04], cta=True, fala="(sem fala)",
         imagem="Rozenhoedkaai com o Belfort + placa do DS `MANDA PRA QUEM VAI →`", transicao="Chegada da placa (DS)", som="clack da placa (−6 dB); trilha fecha"),
]

TAMANHOS = {"full": (1080, 1920), "meia": (1080, 960), "grade": (540, 960)}


def duracao_take(arq):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          os.path.join("fonte", "clipes", arq)], capture_output=True, text=True).stdout
    return float(out)


def extrair(spec):
    arq, entrada, dur, tam, foco, foco2, saida = spec
    w, h = TAMANHOS[tam]
    src = os.path.join("fonte", "clipes", arq)
    info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                           "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", src],
                          capture_output=True, text=True).stdout
    st = json.loads(info)["streams"][0]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    sw, sh = st["width"], st["height"]
    if abs(rot) == 90:
        sw, sh = sh, sw
    hdr = st.get("color_transfer") == "arib-std-b67"
    # escala para cobrir (cover) e recorte no foco; pan linear do foco ao foco2
    escala = max(w / sw, h / sh)
    ew, eh = math.ceil(sw * escala / 2) * 2, math.ceil(sh * escala / 2) * 2
    f2 = foco if foco2 is None else foco2
    xexpr = f"(iw-{w})*({foco}+({f2}-{foco})*min(t/{dur:.3f}\\,1))"
    yexpr = f"(ih-{h})/2"
    vf = (TM + "," if hdr else "") + f"scale={ew}:{eh}:flags=lanczos,crop={w}:{h}:{xexpr}:{yexpr},fps={FPS},format=yuv420p"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{entrada:.3f}", "-t", f"{dur:.3f}", "-i", src, "-vf", vf, "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", saida]
    subprocess.run(cmd, check=True)
    return saida


# ------------------------------------------------------------------------------------------------
# Legendas: grupos de 1 a 4 palavras (até ~24 caracteres), quebra em pontuação, sem terminar em palavra
# funcional (FORMATOS_REELS 6). O texto segue a fala gravada; correções de transcrição ficam listadas.
# ------------------------------------------------------------------------------------------------
CORRECOES = {  # transcrição automática → texto da legenda (validar na escuta)
    ("falando", "Manneken"): "fazendo",
}
FUNCIONAIS = {"a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "que", "em", "na", "no", "um", "uma", "pra", "para",
              "se", "sua", "por", "com", "eu", "te", "essa", "aquela", "aquele", "nós", "mais", "já", "foi", "é", "tá", "não", "só",
              "muito", "alguma", "aí", "dos", "tem", "você", "sabe", "enquanto", "ser", "tava", "estar"}
DESTAQUES = {"superestimada", "decepciona", "bruxelas", "bonita", "comida", "falta", "manneken", "decepcionantes", "injusto",
             "beleza", "grand", "monte", "waffles", "cervejas", "molho", "sal", "trem", "bruges", "cara", "faltando", "europa",
             "pedra", "canais", "medievais", "maravilhosas", "chocolate", "filme", "ruim", "tempero", "tudo", "belgica", "durma",
             "procurando", "sensacao", "dia", "lindo", "linda", "maravilhoso", "boas", "gostosos", "dois"}
JUNTOS = [("grand", "place"), ("manneken", "pis"), ("monte", "das"), ("das", "artes"), ("sem", "sal"), ("dois", "dias"), ("um", "molho"), ("um", "trem"), ("um", "filme")]


def legendas(cortes):
    palavras = [dict(p) for p in PAL if p["s"] >= t_e1 - 0.01]  # o gancho (texto grande) cobre o início
    for i, p in enumerate(palavras):
        for (errada, contexto), certa in CORRECOES.items():
            if norm(p["w"]) == errada and any(norm(x["w"]) == norm(contexto) for x in palavras[max(0, i - 4):i]):
                p["w"] = certa
        if norm(p["w"]) == "porque" and p["s"] < 5:
            p["w"] = "por que"
    # frases: quebram em pontuação ou pausa > 0,35 s
    frases, atual = [], []
    for i, p in enumerate(palavras):
        atual.append(p)
        prox = palavras[i + 1] if i + 1 < len(palavras) else None
        corte_entre = prox is not None and any(p["s"] + 0.25 < c <= prox["s"] - ANTES + 0.02 for c in cortes)
        if prox is None or re.search(r"[,.?!]$", p["w"]) or prox["s"] - p["e"] > 0.35 or corte_entre:
            frases.append(atual)
            atual = []

    def custo(g, ate):
        texto = " ".join(x["w"] for x in g)
        n, ch = len(g), len(texto)
        if n > 5 or ch > 26:
            return 1e9
        c = (24 - ch) ** 2 * 0.15 if ch < 24 else (ch - 24) * 40
        if n == 5:
            c += 30
        if n == 1 and len(g[0]["w"]) < 7:
            c += 60
        if norm(g[-1]["w"]) in FUNCIONAIS and not re.search(r"[,.?!]$", g[-1]["w"]):
            c += 400
        dur = ate - g[0]["s"]  # tempo na tela: até a próxima palavra
        if dur < 0.5:
            c += 250 + (0.5 - dur) * 600
        return c

    def corta(fr):
        n = len(fr)
        melhor = [0.0] + [1e18] * n
        de = [0] * (n + 1)
        for j in range(1, n + 1):
            for i in range(max(0, j - 5), j):
                g = fr[i:j]
                c = custo(g, fr[j]["s"] if j < n else fr[-1]["e"] + 0.2)
                # não separar pares fixos (Grand Place, Manneken Pis…)
                if i > 0 and (norm(fr[i - 1]["w"]), norm(fr[i]["w"])) in JUNTOS:
                    c += 500
                if melhor[i] + c < melhor[j]:
                    melhor[j] = melhor[i] + c
                    de[j] = i
        grupos, j = [], n
        while j > 0:
            grupos.append(fr[de[j]:j])
            j = de[j]
        return grupos[::-1]

    grupos = [g for fr in frases for g in corta(fr)]
    out = []
    for gi, g in enumerate(grupos):
        ini = g[0]["s"] - 0.04
        prox_ini = grupos[gi + 1][0]["s"] - 0.04 if gi + 1 < len(grupos) else None
        fim = g[-1]["e"] + 0.25
        if prox_ini is not None:
            fim = min(fim, prox_ini) if prox_ini - g[-1]["e"] > 0.6 else prox_ini
        texto = " ".join(x["w"] for x in g)
        texto = re.sub(r"[,.]$", "", texto)
        dest = next((x["w"].strip(",.?") for x in g if norm(x["w"]) in DESTAQUES), None)
        if dest and norm(dest) in ("grand", "manneken", "monte", "sem"):
            par = {"grand": "Grand Place", "manneken": "Manneken Pis", "monte": "Monte das Artes", "sem": "sem sal"}[norm(dest)]
            if par.lower() in texto.lower():
                dest = par
        out.append(dict(texto=texto, destaque=dest, ini=q(ini), fim=q(fim)))
    return out


# ------------------------------------------------------------------------------------------------
# Mapa: contorno real (Natural Earth 1:50m) em projeção equirretangular corrigida pela latitude
# ------------------------------------------------------------------------------------------------
BRUXELAS = (4.3525, 50.8467)   # Grand-Place
BRUGES = (3.2247, 51.2093)     # Markt
CAIXA = dict(x=110, y=380, w=860)


def mapa():
    g = json.load(open("rev1/mapa/belgica_naturalearth_50m.json"))
    anel = g["coordinates"][0]
    lat0 = 50.6
    k = math.cos(math.radians(lat0))
    xs = [p[0] * k for p in anel]
    ys = [p[1] for p in anel]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    esc = CAIXA["w"] / (x1 - x0)
    h = (y1 - y0) * esc

    def P(lon, lat):
        return (round(CAIXA["x"] + (lon * k - x0) * esc, 1), round(CAIXA["y"] + (y1 - lat) * esc, 1))

    d = "M" + " L".join(f"{P(*p)[0]},{P(*p)[1]}" for p in anel) + " Z"
    return dict(caminho=d, altura=round(h), bruxelas=P(*BRUXELAS), bruges=P(*BRUGES), caixa=CAIXA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-clipes", action="store_true")
    ap.add_argument("--so", default="", help="extrai só os planos cujo nome contém este texto (ex.: s07)")
    a = ap.parse_args()
    os.makedirs("public/clipes", exist_ok=True)

    # ids sequenciais (s01…) e limites de cada cena em quadros
    for i, c in enumerate(CENAS):
        c["id"] = f"s{i + 1:02d}_" + c["id"].split("_", 1)[1]
    for i, c in enumerate(CENAS):
        c["ini_q"] = corte(c["ini"]) if c["ini"] > 0 else 0
    for i, c in enumerate(CENAS):
        c["fim_q"] = CENAS[i + 1]["ini_q"] if i + 1 < len(CENAS) else q(DUR_TOTAL)
    total_q = q(DUR_TOTAL)

    tarefas, avisos = [], []
    props_cenas = []
    for c in CENAS:
        tipo = c.get("tipo", "video")
        dur_cena = (c["fim_q"] - c["ini_q"]) / FPS
        pc = dict(id=c["id"], tipo=tipo, ini=c["ini_q"], fim=c["fim_q"], cidade=c["cidade"])
        for chave in ("zoom", "origem", "luz", "grade_quente", "modo", "cta", "entrada", "brilho"):
            if chave in c:
                pc[chave] = c[chave]
        if "zoom_kf" in c:
            pc["zoom_kf"] = dict(t=[q(t - ANTES) for t, _ in c["zoom_kf"]], z=[z for _, z in c["zoom_kf"]])
        if "desat" in c:
            d0, d1, sat = c["desat"]
            pc["desat"] = dict(ini=q(d0 - ANTES), fim=q(d1), sat=sat)
        if "cinema" in c:
            pc["cinema"] = q(c["cinema"] - 0.1)
        if tipo == "mapa":
            m = mapa()
            if c["modo"] == "belgica":
                m.update(marcos=dict(belgica=q(W("Bélgica") - ANTES), ponto=q(t_foi_em - ANTES)))
            else:
                m.update(marcos=dict(linha=q(t_conhecer - ANTES), bruges=q(t_bruges1 - ANTES)))
            pc["mapa"] = m
        planos = []
        for j, p in enumerate(c.get("planos", [])):
            if tipo == "video":
                tam = "full"
            elif tipo == "grade":
                tam = "grade"
            elif tipo == "split":
                tam = "meia"
            else:  # comparar: o 1º plano é tela cheia, os outros dois são metades
                tam = "full" if j == 0 else "meia"
            entra_q = q(p["entra"] - ANTES) if "entra" in p else c["ini_q"]
            # o plano fica na tela da sua entrada até o fim da cena (no comparar, o 1º sai na divisão)
            fim_plano = c["fim_q"]
            if tipo == "comparar" and j == 0:
                fim_plano = q(c["planos"][1]["entra"] - ANTES)
            dur = (fim_plano - entra_q) / FPS + 0.4  # folga: dissolve e arredondamento de quadro
            disp = duracao_take(p["arq"]) - p["entrada"]
            if dur > disp + 0.01 and dur - 0.28 <= disp:
                dur = disp  # a folga não cabe no take: usa até o fim
            elif dur > disp + 0.01:
                avisos.append(f"{c['id']}: {p['arq']} precisa de {dur:.2f} s e o take tem {disp:.2f} s a partir de {p['entrada']}")
                dur = disp
            nome = f"{c['id']}_{j}_{os.path.splitext(p['arq'])[0]}.mp4"
            saida = os.path.join("public", "clipes", nome)
            tarefas.append((p["arq"], p["entrada"], dur, tam, p["foco"], p.get("foco2"), saida))
            planos.append(dict(arquivo=f"clipes/{nome}", entra=entra_q, fim=fim_plano, cidade=p.get("cidade", c["cidade"]),
                               rotulo=p.get("rotulo"), take=p["arq"], entrada=p["entrada"]))
        pc["planos"] = planos
        props_cenas.append(pc)

    # noticia (s09): entra em "considerado", marca-texto em "decepcionantes", sai em "Mas"
    noticia = dict(arquivo="recorte_vrt_2012.png", entra=q(t_considerado - ANTES), destaque=q(t_decep - ANTES), sai=q(t_mas2 - ANTES),
                   largura=940, larguraImg=1317, alturaImg=1080,
                   marca=dict(x=60, y=330, w=1136, h=102))  # linha 2 da manchete: most disappointing sight" (medida no recorte)

    for pc in props_cenas:  # fundo da notícia desfoca enquanto o recorte está na tela
        if pc["id"].endswith("_noticia"):
            pc["desfoque"] = dict(ini=noticia["entra"], fim=noticia["sai"])


    gancho = dict(ate=corte(t_entendi), linhas=[
        dict(texto="A CIDADE MAIS", em=q(W("cidade") - ANTES), tam=104),
        dict(texto="SUPERESTIMADA", em=q(W("superestimada") - ANTES), tam=138, destaque=True),
        dict(texto="DA EUROPA", em=q(W("Europa") - ANTES), tam=104),
    ])

    leg = [l for l in legendas([c["ini_q"] / FPS for c in CENAS[1:]]) if l["ini"] < q(CTA_INI)]
    # sem legenda por baixo do gancho (FORMATOS_REELS 4.1): a 1ª legenda entra quando o texto grande sai
    for l in leg:
        if l["ini"] < gancho["ate"]:
            l["ini"] = gancho["ate"]
    leg = [l for l in leg if l["fim"] > l["ini"]]
    # nenhuma legenda durante o mapa do trem em cima do rótulo? fica: o mapa ocupa y 380–1080, legenda em y 1320
    props = dict(fps=FPS, duracao=total_q, cenas=props_cenas, gancho=gancho, noticia=noticia, legendas=leg,
                 cta=dict(entra=q(CTA_INI), destino="MANDA PRA QUEM VAI"),
                 luz=dict(corte=next(c["ini_q"] for c in CENAS if c.get("luz"))))
    json.dump(props, open("rev1/props_rev1.json", "w"), ensure_ascii=False, indent=1)

    # efeitos e trilha (tempos em s, nível relativo ao loudness da voz)
    virada_s = next(c["ini_q"] for c in CENAS if c.get("luz")) / FPS
    efeitos = dict(
        duracao=round(total_q / FPS, 3),
        virada=round(virada_s, 3),
        sons=[
            dict(arq="design-system/sons/externos/PDX_pagina.wav", t=round(q(t_considerado - ANTES) / FPS, 3), rel_db=-8, motivo="recorte da notícia cai"),
            dict(arq="design-system/sons/externos/PDX_swish.wav", t=round(q(t_decep - ANTES) / FPS + 0.05, 3), rel_db=-10, motivo="marca-texto na manchete"),
            dict(arq="design-system/sons/externos/PDX_swish.wav", t=round(q(t_conhecer - ANTES) / FPS + 0.1, 3), rel_db=-6, motivo="linha do trem corre no mapa"),
            dict(arq="design-system/sons/externos/PDX_riser.wav", fim=round(virada_s + 0.12, 3), rel_db=-8, motivo="sobe até a virada (termina no pico da luz)"),
            dict(arq="design-system/sons/externos/PDX_ar_longo.wav", t=round(virada_s - 0.05, 3), rel_db=-6, motivo="luz de passagem na virada"),
            dict(arq="design-system/sons/externos/PDX_swish.wav", t=round(q(t_bruges2 - ANTES) / FPS, 3), rel_db=-6, motivo="tela divide Bruxelas × Bruges"),
            dict(arq="design-system/sons/PD_clack_v1.wav", t=round(q(CTA_INI) / FPS + 0.28, 3), rel_db=-6, motivo="placa do CTA assenta (Chegada, 280 ms) — único som do DS"),
        ],
        trilha=[
            dict(arq="fonte/musica/Investigations.mp3", reel_ini=0.0, faixa_ini=0.0, reel_fim=round(t_ate + 0.3, 3), fade_in=0.0, fade_out=0.9,
                 credito='"Investigations" Kevin MacLeod (incompetech.com), CC BY 4.0'),
            dict(arq="fonte/musica/Reunited.mp3", reel_ini=round(t_ate - 0.1, 3), faixa_ini=round(37.5 - (virada_s - (t_ate - 0.1)), 3),
                 reel_fim=round(t_nao - 0.15, 3), fade_in=1.2, fade_out=1.4,
                 credito='"Reunited" Kevin MacLeod (incompetech.com), CC BY 4.0', nota="o trecho que 'abre' (37,5 s da faixa) cai na virada"),
            dict(arq="fonte/musica/Reunited.mp3", reel_ini=round(t_nao - 0.15 - 1.4, 3), faixa_ini=0.0, reel_fim=round(total_q / FPS, 3), fade_in=1.4, fade_out=1.6,
                 credito='"Reunited" Kevin MacLeod (incompetech.com), CC BY 4.0', nota="fechamento: volta ao tema de abertura da faixa"),
        ],
        fala=[[round(p["s"], 3), round(p["e"], 3)] for p in PAL],
    )
    json.dump(efeitos, open("rev1/efeitos_rev1.json", "w"), ensure_ascii=False, indent=1)

    # roteiro de cortes
    linhas = ["# Roteiro de cortes · REV1", "",
              f"Duração: {total_q / FPS:.2f} s ({total_q} quadros a {FPS} qps). Voz decupada: {DUR_VOZ:.2f} s. "
              "Tempos = corte da cena (0,08 s antes da palavra). Gerado por `rev1/montar_rev1.py`.", "",
              "| # | Tempo | Fala (gravada) | Imagem | Take (entrada) | Transição | Som |", "|---|---|---|---|---|---|---|"]
    for i, c in enumerate(CENAS):
        t0, t1 = c["ini_q"] / FPS, c["fim_q"] / FPS
        takes = ", ".join(f"{p['arq']} ({p['entrada']:.1f} s)" for p in c.get("planos", [])) or "animação"
        linhas.append(f"| {i + 1} | {t0:.2f}–{t1:.2f} s ({t1 - t0:.2f} s) | {c['fala']} | {c['imagem']} | {takes} | {c['transicao']} | {c['som']} |")
    open("rev1/roteiro_de_cortes_rev1.md", "w").write("\n".join(linhas) + "\n")

    for av in avisos:
        print("AVISO", av)
    curtas = [(c["id"], (c["fim_q"] - c["ini_q"]) / FPS) for c in CENAS if (c["fim_q"] - c["ini_q"]) / FPS < 2.0]
    print(f"{len(CENAS)} cenas · {total_q} quadros ({total_q / FPS:.2f} s) · {len(leg)} legendas")
    print("cenas abaixo de 2 s:", ", ".join(f"{i} {d:.2f}s" for i, d in curtas) or "nenhuma")

    if not a.sem_clipes:
        if a.so:
            tarefas = [t for t in tarefas if a.so in t[-1]]
        with ThreadPoolExecutor(max_workers=3) as ex:
            for s in ex.map(extrair, tarefas):
                print("ok", s)


if __name__ == "__main__":
    main()
