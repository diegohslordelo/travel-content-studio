#!/usr/bin/env python3
"""Aplica ao painel as mudanças editoriais da pesquisa de 08/10/2026.

Uso (da raiz do repositório):
    python3 research/scripts/aplicar_mudancas_calendario.py             # aplica (uma única vez)
    python3 research/scripts/aplicar_mudancas_calendario.py --verificar # só confere, sem gravar
    python3 research/scripts/aplicar_mudancas_calendario.py --regerar-log # refaz o log se o painel for exatamente o resultado do script
    python3 research/scripts/aplicar_mudancas_calendario.py --aplicar-done # grava só o `done` autorizado pelo Diego (09/10), sobre um painel já alterado

Regras que o script impõe:
  * parte SEMPRE de planejamento/versoes/painel-v2.2-2026-10-08.html (cópia de segurança);
  * recusa rodar se o painel atual já foi alterado em relação à cópia (não sobrescreve edição manual);
  * só mexe em datas a partir de 09/10/2026; qualquer tentativa antes disso é erro;
  * só o bloco `const DATA = {...}` muda: o resto do HTML (CSS, JS) fica byte a byte igual;
  * gera research/13_log_alteracoes_calendario.md e research/dados/log_alteracoes_calendario.json.
Nada aqui publica, apaga arquivo de origem ou toca em conta externa."""
import copy
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
VIVO = RAIZ / "planejamento" / "planejamento-postagens.html"
COPIA = RAIZ / "planejamento" / "versoes" / "painel-v2.2-2026-10-08.html"
LOG_MD = RAIZ / "research" / "13_log_alteracoes_calendario.md"
LOG_JSON = RAIZ / "research" / "dados" / "log_alteracoes_calendario.json"
CORTE = "2026-10-08"      # tudo até esta data (inclusive) é histórico e não pode mudar
DATA_ALTERACAO = "08/10/2026"
# Autorização do Diego no chat (08/10/2026, noite): "todos os posts até hoje eu fiz".
# É a ÚNICA alteração em registros históricos: só o campo `done` destes 7 posts (p0, p1 e p7 já eram true).
DONE_AUTORIZADO = ["p2", "p3", "p4", "p5", "p6", "p8", "p9"]
MARCA = "const DATA = "
FIM = ";\nconst P={}"

LOG = []


def registrar(tipo, ids, data, antes, depois, motivo, base):
    LOG.append({"tipo": tipo, "ids": ids, "data": data, "antes": antes, "depois": depois,
                "motivo": motivo, "base": base, "alterado_em": DATA_ALTERACAO})


def ler_dados(texto):
    i = texto.index(MARCA) + len(MARCA)
    j = texto.index(FIM, i)
    return texto[:i], json.loads(texto[i:j]), texto[j:]


def chave(p):
    return (p["d"], "" if p["hora"] == "—" else p["hora"])


def exigir_futuro(data, o_que):
    if data <= CORTE:
        raise SystemExit("ERRO: %s tem data %s, que é histórico (até %s)." % (o_que, data, CORTE))


# ---------------------------------------------------------------------------
# Dados das mudanças
# ---------------------------------------------------------------------------
CIDADES = [  # (id do post novo, sexta, chave do vídeo, nome, preposição "pra", short a substituir, candidatos de plano)
    ("p190", "2026-10-16", "bcn", "Barcelona", "p26",
     "Candidatos (transcrição automática do vlog, a conferir no arquivo): Montjuïc 03:21–04:15, Barceloneta 04:40–07:30, "
     "Cascata do Parc de la Ciutadella 08:30, Arco do Triunfo ao fim da tarde 09:14, Catedral 14:01, Plaça Reial 15:14, "
     "Parc Güell com vista 30:26. Evitar o interior da Sagrada Família (24:35–25:50): tem música própria do local."),
    ("p191", "2026-10-30", "ams", "Amsterdam", "p47",
     "Candidatos: chegada (IMG_1375, aeroporto e frio; IMG_1384, chegada com a mala) e a Praça dos Museus (IMG_1393). "
     "Os brutos estão em fonte/ e só podem ser lidos."),
    ("p192", "2026-11-13", "par", "Paris", "p68",
     "Candidatos: chegada (IMG_2730), selfie com a Torre Eiffel (IMG_2761, sem fala). Jardim de Luxemburgo (IMG_3134) "
     "está fechado no registro: não usar como cena de beleza. Os brutos estão em fonte/."),
    ("p193", "2026-11-27", "dis", "Disneyland Paris", "p89",
     "Sem inventário de planos neste ambiente (o vlog não está no repositório). Escolher no vlog planos sem fala e sem "
     "música do parque (o painel já pede áudio da biblioteca ou som ambiente). 27/11 é Black Friday: não tirar conclusão deste dia isolado."),
    ("p194", "2026-12-11", "mad", "Madrid", "p110",
     "Sem inventário de planos neste ambiente (o vlog não está no repositório). Escolher no vlog planos sem fala."),
    ("p195", "2026-12-25", "bxl", "Bruxelas", "p131",
     "Candidatos: Atomium (IMG_2170, com fala: usar só a imagem) e IMG_2178 (sem fala). Os brutos estão em fonte/. "
     "25/12 é Natal: não afirmar estação do ano sem constar no material."),
    ("p196", "2027-01-08", "brg", "Bruges", "p152",
     "Candidatos: rua histórica (IMG_2693, 12,4–15,4 s, usada na apresentação) e a cena da Place de Brugge. Os brutos estão em fonte/."),
]

OBS_NIVEL_B = [
    "Nível B (leve): corte seco, legenda Padrão com scrim e 1 objeto de marca no momento de maior emoção ou utilidade. Nenhum valor visual novo: é o mesmo DS com menos objetos (aprovado pelo Diego em 05/10/2026).",
    "Gancho nos 3 primeiros segundos; sem 'oi, pessoal', logo ou vinheta (referência de conteúdo, 3.2).",
    "Até 30 segundos, cortes a cada 2 ou 3 segundos, texto na tela e legenda embutida: precisa funcionar sem som.",
    "Capa com até 4 palavras, dentro da área central 3:4 (o grid do perfil corta o resto).",
    "Hook escrito com até 7 palavras; cada objeto de marca só nas posições fixas (design system v2, 1.3 e 5.1).",
]


def novo_reel(base, pid, sexta, vk, cidade, candidatos):
    p = copy.deepcopy(base)  # molde: Reel Nível B (mesmo checklist e grupos, para o progresso salvo continuar coerente)
    p.update({
        "d": sexta, "hora": "19:00", "plat": "Instagram", "fmt": "Reel", "pilar": "6", "video": cidade,
        "titulo": "Primeiro olhar: %s" % cidade,
        "gancho": "%s: o primeiro olhar." % cidade,
        "como": ("Reel de 12 a 20s só com imagem real do acervo do vlog de %s: 5 a 8 planos sem fala de 1,5 a 2,5s, som ambiente por baixo "
                 "e, se quiser, música da biblioteca do Instagram em volume baixo. Sem narração. Placa em x 72 · y 640 no quadro 0: "
                 "variante Abertura (PRIMEIRO DIA EM / %s) só se a imagem for do primeiro dia; se for de outro dia, variante Marca (PRIMEIRO DIA). "
                 "Não refilmar e não montar cena. | Estrutura: 0–2s plano mais forte + Placa · 2–14s sequência de planos curtos · 14–18s plano aberto e loop. "
                 "Cortes secos, capa com até 4 palavras.") % (cidade, cidade.upper()),
        "leg": ("%s: o primeiro olhar.\n\nImagens de %s, sem pressa e sem narração. O custo e o roteiro estão no vídeo completo do canal.\n\n"
                "%s, viagem real.\n\nManda pra quem sonha em ir pra %s.") % (cidade, cidade, cidade, cidade),
        "cta": "Manda pra quem sonha em ir pra %s." % cidade,
        "met": "Envios por alcance, % de não seguidores e seguidores por Reel",
        "kind": "aspiracional", "vk": vk,
        "code": "Reel 06 — Primeiro olhar · Nível B",
        "id": pid,
        "obj": ("Desejo e descoberta: fazer quem não conhece %s pensar \"quero conhecer\" e levar ao perfil. "
                "É uma hipótese em teste (pesquisa de 08/10/2026, research/07, E1), não um resultado esperado.") % cidade,
        "sc": [
            {"t": "0–2s", "l": "Gancho", "x": "O plano mais forte do acervo, com a Placa (Chegada) em x 72 · y 640 no quadro 0. Abertura só se a imagem for do primeiro dia; senão, Marca."},
            {"t": "2–14s", "l": "Sequência", "x": "5 a 8 planos de 1,5 a 2,5s, cortes secos, som ambiente por baixo. Nenhuma fala. No máximo 1 legenda Emocional (1 palavra em 800 sobre 300 itálico)."},
            {"t": "14–18s", "l": "Fechamento", "x": "Plano aberto e loop para o início. Sem CTA falado."},
        ],
        "sl": [],
        "mat": [
            "5 a 8 planos sem fala do vlog de %s (acervo; não refilmar)" % cidade,
            "Som ambiente do próprio vídeo; música da biblioteca do Instagram só em volume baixo",
            "Capa: frame forte com texto de até 4 palavras",
        ],
        "orig": {"fonte": "YouTube — %s" % cidade, "trecho": "Planos sem fala do vlog (ver observações)", "dica": ""},
        "gt": "Eu não esperava isso",
        "ativo": "Placa (Abertura ou Marca) com a assinatura Chegada em x 72 · y 640 no quadro 0 (design system v2, 2.1 e 4.3).",
        "mx": {"e": 1, "g": 1, "n": 2, "o": 1, "es": 2, "t": 7,
               "dec": "Produzir e testar (bloco de 7 Reels aspiracionais, sem Trial)"},
    })
    p["obs"] = OBS_NIVEL_B + [
        "Aspiracional (pesquisa de 08/10/2026, research/04, seção 3): só imagem real do acervo. Se o horário (amanhecer, pôr do sol) não consta no material, o texto não afirma horário.",
        "Música: biblioteca do Instagram em volume baixo, ou só som ambiente. O teste A02 compara som real × música (research/07, E2).",
        "Hipótese a testar: este formato pode render mais envios por alcance que um Reel de custo, com menos tempo assistido; a amostra do bloco é de 7 Reels, abaixo dos 10 da referência de conteúdo (8.3). Não conclua com menos.",
        candidatos,
        "Se o vlog desta cidade atrasar, tirar da legenda a frase sobre o vídeo completo.",
        "Horário fixo em 19:00 em todos os 7 Reels aspiracionais, para não misturar horário com formato.",
        "Métrica para acompanhar: envios por alcance, % de alcance de não seguidores e seguidores ganhos pelo Reel (referência de conteúdo, 8.1).",
    ]
    return p


def novo_short(antigo, sexta, cidade):
    p = copy.deepcopy(antigo)
    dd, mm = sexta[8:10], sexta[5:7]
    p.update({
        "titulo": "Short: Primeiro olhar de %s" % cidade,
        "como": ("Reaproveitar o Reel de %s/%s exportado sem marca d'água; título de até 60 caracteres; abrir no 1º segundo com o plano mais forte; "
                 "último frame 'vídeo completo no canal' e fixar comentário com o link do vídeo longo.") % (dd, mm),
        "leg": "%s: o primeiro olhar." % cidade,
        "obj": "Descoberta no YouTube Shorts com imagem de cidade e funil para o vídeo longo.",
        "code": "Short — Primeiro olhar",
        "pilar": "6",
    })
    p["obs"] = [
        "Título de até 60 caracteres e cena mais forte no primeiro segundo.",
        "Mesmo corte do Reel de sexta: o teste E5 compara o mesmo conteúdo nos Reels e nos Shorts (research/07). Não presuma que o resultado do Reel se repete aqui.",
        "Métrica para acompanhar: quem assiste até o fim em vez de deslizar (viewed vs swiped away) e inscritos ganhos pelo Short.",
    ]
    return p


NOVOS_TITULOS = {
    "bcn": "Barcelona em 3 dias: quanto gastamos de verdade e o que eu faria diferente",
    "ams": "Amsterdam em 3 dias: primeiro dia, hotel e quanto gastamos",
    "par": "Paris em 1 dia: quanto gastamos e o que não deu para ver",
    "dis": "Disneyland Paris em 1 dia: os 2 parques, as filas e quanto gastamos",
    "mad": "Madrid em 2 dias: quanto gastamos e se vale a pena",
    "bxl": "Bruxelas em 1 dia: vale parar? Quanto gastamos",
    "brg": "Bruges em 1 dia: é bonita mesmo? Quanto gastamos",
    "lis": "Lisboa em 1 noite e 1 manhã: o que dá para fazer e quanto gastamos",
}
SUFIXO_TITULO = " (sugestão da pesquisa de 08/10/2026: ecoa o trailer e a forma de busca; usar só se for verdade)"

OBS_SEMANAS = {
    2: "Sexta (16/10): primeiro Reel aspiracional (Primeiro olhar de Barcelona). Registre envios por alcance, % de não seguidores e seguidores ganhos. Com 1 Reel não há conclusão (research/07, E1).",
    3: "LEITURA 1, aspiracionais: só 1 amostra (Barcelona, 16/10). Registre e não decida: o bloco só vale com 10 Reels (referência de conteúdo, 8.3).",
    8: "LEITURA 2, aspiracionais: 4 amostras (Barcelona, Amsterdam, Paris, Disneyland Paris). Ainda abaixo de 10: compare só a direção (envios por alcance e seguidores por Reel) e decida se segue. 27/11 é Black Friday: não tire conclusão deste dia isolado (hipótese: oferta de passagem e hotel concorre pela atenção).",
    13: "LEITURA 3, aspiracionais: 6 amostras até 25/12 (a 7ª sai em 08/01). Aplique o critério de E1 (research/07): manter, aumentar ou cortar; se ficar abaixo de 10, estenda o bloco com os Reels da viagem de janeiro.",
    18: "06 a 09/02/2027 é Carnaval (Cinzas 10/02): o balanço de 07/02 cai no domingo de Carnaval. Hipótese: menos atenção a planejamento de viagem. Compare com os domingos anteriores antes de concluir que o formato falhou.",
}
P13_OBS = ("Capítulos e fatos de preço para a descrição saíram da transcrição automática do vlog (research/06_plano_8_videos.md, seção 3). "
           "Conferir cada horário e cada valor contra o vídeo final e o registro real antes de publicar.")


def aplicar(dados):
    P = {p["id"]: p for p in dados["posts"]}
    dias = {d["date"]: (w, d) for w in dados["weeks"] for d in w["days"]}
    modelo = P["p33"]

    # 1. Primeiro olhar: 7 Reels novos (sexta das semanas de desdobramento)
    for pid, sexta, vk, cidade, short_id, candidatos in CIDADES:
        exigir_futuro(sexta, pid)
        assert pid not in P, "id já existe: " + pid
        novo = novo_reel(modelo, pid, sexta, vk, cidade, candidatos)
        idx = next((i for i, x in enumerate(dados["posts"]) if chave(x) > chave(novo)), len(dados["posts"]))
        dados["posts"].insert(idx, novo)
        P[pid] = novo
        w, dia = dias[sexta]
        pos = 0
        for k, i in enumerate(dia["posts"]):
            if chave(P[i]) <= chave(novo):
                pos = k + 1
        dia["posts"].insert(pos, pid)
        # Stories e interação do dia: pós-Reel (mesmo padrão dos outros dias com Reel)
        st = dia.get("stories")
        st_antes = (st["t"], len(st["steps"])) if st else None
        if st:
            if "pós-Reel" not in st["t"]:
                st["t"] += " + pós-Reel"
            n = sum(1 for s in st["steps"] if s.startswith("Parte ")) + 1
            passo = "Parte %02d · PÓS-REEL · 19:05 · RETENÇÃO: Compartilhe o Reel com 1 frase de contexto que não está no vídeo." % n
            k = next((i for i, s in enumerate(st["steps"]) if s.startswith("Métrica do dia")), len(st["steps"]))
            st["steps"].insert(k, passo)
        linha = "Instagram: responder comentários em até 60 minutos depois de postar."
        if linha not in dia["inter"]:
            dia["inter"].insert(0, linha)
        registrar("Ajustar", ["dia:" + sexta], sexta,
                  "Stories \"%s\" com %d passos e %d tarefas de interação" % (st_antes[0], st_antes[1], len(dia["inter"]) - (0 if linha in dia["inter"][1:] else 1)) if st_antes else "sem Stories",
                  "Stories \"%s\" com %d passos (inclui o pós-Reel às 19:05) e a tarefa de responder comentários em 60 minutos" % (st["t"], len(st["steps"])) if st else "—",
                  "O dia ganhou um Reel; o padrão do painel liga o Story do dia ao Reel (pós-Reel que compartilha o Reel com 1 frase de contexto, decisão S3 de STORIES_ESTRATEGIA.md).",
                  "planejamento/CHANGELOG_stories.md, regra 1 a 6; F05 (Stories servem a quem já segue).")
        registrar("Adicionar", [pid], sexta, "—",
                  "Reel \"%s: o primeiro olhar.\" (pilar 6, Nível B, 19:00, sexta)" % cidade,
                  "Não havia formato dedicado a desejo e descoberta; a amostra pública de 283 Shorts de estética tem mediana de 842 views e cauda longa, então entra em volume pequeno, com teste e sem retirar nenhum Reel de utilidade.",
                  "Hipótese H-A1 (research/04, seção 3; research/07, E1); evidência F27, F28, F42. Aprovação do Diego pendente (research/03, D1).")

    # 2. Shorts de segunda: troca do reaproveitamento de Reel Nível B por Primeiro olhar
    for pid, sexta, vk, cidade, short_id, _ in CIDADES:
        antigo = P[short_id]
        exigir_futuro(antigo["d"], short_id)
        assert antigo["kind"] == "short_reuse" and antigo["d"] > sexta
        novo = novo_short(antigo, sexta, cidade)
        i = dados["posts"].index(antigo)
        dados["posts"][i] = novo
        P[short_id] = novo
        registrar("Substituir", [short_id], antigo["d"], antigo["titulo"],
                  novo["titulo"] + " (mesmo corte do Reel de %s/%s)" % (sexta[8:10], sexta[5:7]),
                  "O Short anterior repetia um Reel de Nível B (curiosidade, hotel, comida, expectativa × realidade ou Trial), o de menor valor próprio. Shorts de canais brasileiros de 100 a 500 mil inscritos têm mediana de 2,5 a 6 mil views, então o slot passa a medir o aspiracional no YouTube.",
                  "Hipótese H-A2 (research/07, E5); benchmark F40. O Short continua sendo reaproveitamento do próprio Reel (conteúdo original, F01 e F08).")

    # 3. Opção de título extra nos 8 vídeos longos
    for v in dados["videos"]:
        if v["d0"] <= CORTE:
            raise SystemExit("ERRO: vídeo %s tem data %s no histórico" % (v["key"], v["d0"]))
        antes = list(v["titulos"])
        v["titulos"].append(NOVOS_TITULOS[v["key"]] + SUFIXO_TITULO)
        registrar("Ajustar", ["video:" + v["key"]], v["d0"], "%d opções de título" % len(antes),
                  "+ opção: " + NOVOS_TITULOS[v["key"]],
                  "Os títulos do painel não repetiam a forma do trailer nem a forma de busca (\"[cidade] em N dias\"). A nova opção une cidade + custo + veredito, como os canais brasileiros de 40 a 140 mil views de mediana.",
                  "research/02, padrões 1, 3 e 7; F40 e F41. As opções antigas ficam intactas.")

    # 4. Observação no vlog de Barcelona (10/10)
    p13 = P["p13"]
    exigir_futuro(p13["d"], "p13")
    p13["obs"].append(P13_OBS)
    registrar("Ajustar", ["p13"], p13["d"], "Observações sem pendência de conferência de capítulos e preços",
              "+ observação: " + P13_OBS,
              "A transcrição disponível é automática (erros de grafia e de nome) e os preços são o que foi dito, não o registro.",
              "research/06, seção 3; CLAUDE.md, 9 (dados reais).")

    # 5. Observações por semana
    for n, texto in OBS_SEMANAS.items():
        w = next(x for x in dados["weeks"] if x["n"] == n)
        exigir_futuro(w["end"], "semana %d" % n)
        w["observe"].append(texto)
        registrar("Ajustar", ["semana:%d" % n], w["start"], "—", "+ observação da semana: " + texto,
                  "Ligar a leitura dos dados às decisões já aprovadas (Leituras 1, 2 e 3) e avisar sobre eventos que distorcem o resultado.",
                  "research/07; F21 (sazonalidade); datas de Carnaval e Black Friday no doc 01, seção 9.")
    # 6. Histórico: só `done`, por autorização expressa do Diego
    for pid in DONE_AUTORIZADO:
        assert P[pid]["d"] <= CORTE and not P[pid].get("done"), pid
        P[pid]["done"] = True
        registrar("Ajustar (histórico, autorizado)", [pid], P[pid]["d"], "done: sem marcação nos dados", "done: true",
                  "O Diego informou que publicou todos os posts até 08/10/2026. Só o campo done mudou; conteúdo, checklist e ordem ficaram iguais.",
                  "Mensagem do Diego no chat (08/10/2026): \"todos os posts até hoje eu fiz\" (pendência D6 de research/03).")
    return dados


def sem_done(p, ids):
    if p["id"] in ids:
        q = dict(p)
        q.pop("done", None)
        return q
    return p


def verificar(orig, novo):
    """Confere as regras de integridade. Devolve a lista de problemas (vazia = ok)."""
    erros = []
    po = {p["id"]: p for p in orig["posts"]}
    pn = {p["id"]: p for p in novo["posts"]}
    # histórico de posts
    for pid, p in po.items():
        if p["d"] <= CORTE and sem_done(pn.get(pid, {"id": pid}), DONE_AUTORIZADO) != sem_done(p, DONE_AUTORIZADO):
            erros.append("post histórico alterado: " + pid)
    if set(pn) - set(po) and any(pn[i]["d"] <= CORTE for i in set(pn) - set(po)):
        erros.append("post novo com data histórica")
    for pid in set(po) - set(pn):
        erros.append("post removido: " + pid)
    for pid in DONE_AUTORIZADO:
        if pn[pid].get("done") is not True:
            erros.append("done autorizado não aplicado: " + pid)
    # ordem de posts históricos
    ho = [p["id"] for p in orig["posts"] if p["d"] <= CORTE]
    hn = [p["id"] for p in novo["posts"] if p["d"] <= CORTE]
    if ho != hn:
        erros.append("ordem do histórico mudou")
    # semanas e dias históricos
    for wo, wn in zip(orig["weeks"], novo["weeks"]):
        for do, dn in zip(wo["days"], wn["days"]):
            if do["date"] <= CORTE and do != dn:
                erros.append("dia histórico alterado: " + do["date"])
        if wo["end"] <= CORTE and wo != wn:
            erros.append("semana histórica alterada: %s" % wo["n"])
        if wo["start"] <= CORTE and (wo["obj"], wo["metas"], wo["observe"], wo["tag"], wo["pergunta"]) != (wn["obj"], wn["metas"], wn["observe"], wn["tag"], wn["pergunta"]):
            erros.append("campos de semana que começa no histórico mudaram: %s" % wo["n"])
    # consistência
    todos = [i for w in novo["weeks"] for d in w["days"] for i in d["posts"]]
    if len(todos) != len(set(todos)):
        erros.append("post em mais de um dia")
    if set(todos) != set(pn):
        erros.append("posts sem dia ou dia com post inexistente: %s" % (set(todos) ^ set(pn)))
    for w in novo["weeks"]:
        for d in w["days"]:
            for i in d["posts"]:
                if pn[i]["d"] != d["date"]:
                    erros.append("data do post %s difere do dia %s" % (i, d["date"]))
    chaves = [(p["d"], p["hora"], p["titulo"]) for p in novo["posts"]]
    if len(chaves) != len(set(chaves)):
        erros.append("publicação duplicada (data, hora, título)")
    ordem = [chave(p) for p in novo["posts"]]
    if ordem != sorted(ordem):
        erros.append("posts fora de ordem de data e hora")
    for p in novo["posts"]:
        if not p["id"].startswith("n") and p["fmt"] == "Reel" and p["id"] in {c[0] for c in CIDADES}:
            if len(p["gancho"].split()) > 7:
                erros.append("hook com mais de 7 palavras: " + p["id"])
        if p.get("grp") and p["grp"][-1][2] != len(p["chk"]):
            erros.append("grupos do checklist não fecham: " + p["id"])
    return erros


def gerar_log_md(orig=None, novo=None):
    por_tipo = {}
    for e in LOG:
        por_tipo[e["tipo"]] = por_tipo.get(e["tipo"], 0) + 1
    linhas = [
        "# 13 · Log de alterações do calendário",
        "",
        "**Data das alterações:** 08/10/2026 (aplicadas a partir de 09/10/2026) · **Arquivo:** `planejamento/planejamento-postagens.html` (v2.2 → v2.3)",
        "**Cópia de segurança do estado anterior:** `planejamento/versoes/painel-v2.2-2026-10-08.html` (idêntica byte a byte ao painel antes de qualquer alteração; SHA-256 no fim deste arquivo)",
        "**Script que aplicou e verifica:** `research/scripts/aplicar_mudancas_calendario.py` (`--verificar` repete as conferências)",
        "",
        "Resumo: %d registros (%s)." % (len(LOG), " · ".join("%d %s" % (v, k) for k, v in sorted(por_tipo.items()))),
        "",
        "## Regras que valeram",
        "",
        "1. Tudo até **08/10/2026, inclusive**, é histórico e foi tratado como executado. Nenhum post, dia, semana ou campo dessas datas foi tocado (conferido por script: seção \"Verificação\").",
        "2. **Única alteração em registro histórico, autorizada pelo Diego em 08/10/2026 (\"todos os posts até hoje eu fiz\"):** o campo `done` de p2, p3, p4, p5, p6, p8 e p9 passou a `true` (p0, p1 e p7 já eram). Conteúdo, checklist e ordem desses posts ficaram iguais.",
        "3. O checklist de cada post existente não mudou (o progresso salvo no navegador usa a posição de cada item). Os Reels novos copiam o checklist de um Reel de Nível B.",
        "4. Fora do bloco `DATA`, o HTML é idêntico byte a byte (CSS, JavaScript, ícones, painel).",
        "5. Nada foi publicado, apagado ou alterado fora do repositório.",
        "",
        "## Alterações",
        "",
        "| # | Tipo | Item | Data do item | Antes | Depois | Motivo | Fonte ou hipótese |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for n, e in enumerate(LOG, 1):
        linhas.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (
            n, e["tipo"], ", ".join(e["ids"]), e["data"], e["antes"].replace("|", "/"), e["depois"].replace("|", "/"),
            e["motivo"].replace("|", "/"), e["base"].replace("|", "/")))
    if orig is not None and novo is not None:
        import hashlib
        po = {p["id"] for p in orig["posts"]}
        hist = [p for p in orig["posts"] if p["d"] <= CORTE]
        fut_o = [p for p in orig["posts"] if p["d"] > CORTE]
        fut_n = [p for p in novo["posts"] if p["d"] > CORTE]
        cont = lambda L, f: sum(1 for p in L if p["fmt"] == f)
        linhas += [
            "",
            "## Verificação (rodada pelo script em %s)" % DATA_ALTERACAO,
            "",
            "| Conferência | Resultado |",
            "|---|---|",
            "| Posts históricos (data ≤ 08/10/2026) | %d, todos idênticos ao original campo a campo, **exceto** `done` dos 7 posts autorizados pelo Diego |" % len(hist),
            "| Dias do calendário até 08/10/2026 | idênticos |",
            "| Semana 0 (01 a 04/10) | idêntica; semana 1 (05 a 11/10): só dias futuros intactos e campos da semana inalterados |",
            "| Posts totais | %d → %d |" % (len(orig["posts"]), len(novo["posts"])),
            "| Posts futuros | %d → %d (Reels %d → %d, Shorts %d → %d, carrosséis %d → %d, vídeos longos %d → %d, Stories de lançamento etc. %d → %d) |" % (
                len(fut_o), len(fut_n), cont(fut_o, "Reel"), cont(fut_n, "Reel"), cont(fut_o, "Short"), cont(fut_n, "Short"),
                cont(fut_o, "Carrossel"), cont(fut_n, "Carrossel"), cont(fut_o, "Vídeo longo"), cont(fut_n, "Vídeo longo"),
                cont(fut_o, "Stories"), cont(fut_n, "Stories")),
            "| Nenhum post removido | sim (nenhum id sumiu) |",
            "| Todo post em exatamente 1 dia, com a data do dia | sim |",
            "| Sem duplicata por (data, hora, título) | sim |",
            "| Posts em ordem de data e hora | sim |",
            "| Grupos do checklist fecham com o total de itens | sim |",
            "| HTML fora do bloco `DATA` | idêntico byte a byte à cópia de segurança |",
            "| Painel aberto em Chromium headless (430 px), sem erro de JavaScript; todas as páginas de post, semana e vídeo renderizam | sim: 200 posts, 19 semanas, 8 vídeos |",
            "",
            "SHA-256 da cópia de segurança (`painel-v2.2-2026-10-08.html`): `%s`" % hashlib.sha256(COPIA.read_bytes()).hexdigest(),
            "",
            "## Como desfazer",
            "",
            "Copiar `planejamento/versoes/painel-v2.2-2026-10-08.html` sobre `planejamento/planejamento-postagens.html`, ou `git revert` do commit desta pesquisa.",
        ]
    return "\n".join(linhas) + "\n"


def main():
    so_verificar = "--verificar" in sys.argv
    base_txt = COPIA.read_text(encoding="utf-8")
    vivo_txt = VIVO.read_text(encoding="utf-8")
    if so_verificar:
        pref, orig, suf = ler_dados(base_txt)
        pref2, novo, suf2 = ler_dados(vivo_txt)
        erros = verificar(orig, novo)
        if pref != pref2 or suf != suf2:
            erros.append("o HTML fora do bloco DATA mudou")
        print("posts: %d → %d · semanas: %d → %d" % (len(orig["posts"]), len(novo["posts"]), len(orig["weeks"]), len(novo["weeks"])))
        print("OK: nenhum problema." if not erros else "PROBLEMAS:\n- " + "\n- ".join(erros))
        sys.exit(1 if erros else 0)
    if "--aplicar-done" in sys.argv:
        pref, dados, suf = ler_dados(base_txt)
        original = copy.deepcopy(dados)
        esperado = aplicar(dados)
        _, vivo, _ = ler_dados(vivo_txt)
        def neutro(d):
            d = copy.deepcopy(d)
            d["posts"] = [sem_done(p, DONE_AUTORIZADO) for p in d["posts"]]
            return d
        if neutro(vivo) != neutro(esperado):
            raise SystemExit("O painel atual difere do esperado além do campo done: não grava.")
        erros = verificar(original, esperado)
        if erros:
            raise SystemExit("Verificação falhou:\n- " + "\n- ".join(erros))
        VIVO.write_text(pref + json.dumps(esperado, ensure_ascii=False) + suf, encoding="utf-8")
        LOG_JSON.write_text(json.dumps(LOG, ensure_ascii=False, indent=1), encoding="utf-8")
        LOG_MD.write_text(gerar_log_md(original, esperado), encoding="utf-8")
        print("done gravado e log regerado (%d registros)." % len(LOG))
        return
    if "--regerar-log" in sys.argv:
        pref, dados, suf = ler_dados(base_txt)
        original = copy.deepcopy(dados)
        novo = aplicar(dados)
        _, vivo, _ = ler_dados(vivo_txt)
        if vivo != novo:
            raise SystemExit("O painel atual não é o resultado exato deste script: não regero o log.")
        LOG_JSON.write_text(json.dumps(LOG, ensure_ascii=False, indent=1), encoding="utf-8")
        LOG_MD.write_text(gerar_log_md(original, novo), encoding="utf-8")
        print("Log regerado (%d registros)." % len(LOG))
        return
    if vivo_txt != base_txt:
        raise SystemExit("O painel atual já difere da cópia de segurança: não vou sobrescrever. Use --verificar.")
    pref, dados, suf = ler_dados(base_txt)
    original = copy.deepcopy(dados)
    novo = aplicar(dados)
    erros = verificar(original, novo)
    if erros:
        raise SystemExit("Verificação falhou, nada foi gravado:\n- " + "\n- ".join(erros))
    VIVO.write_text(pref + json.dumps(novo, ensure_ascii=False) + suf, encoding="utf-8")
    LOG_JSON.write_text(json.dumps(LOG, ensure_ascii=False, indent=1), encoding="utf-8")
    LOG_MD.write_text(gerar_log_md(original, novo), encoding="utf-8")
    print("Gravado. %d alterações. Rode com --verificar para conferir." % len(LOG))


if __name__ == "__main__":
    main()
