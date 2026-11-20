"""Relatório da decupagem (revN/DECUPAGEM_REVN.md) a partir de revN/edl_revN.json, da transcrição e das decisões.
Roda de reels/bruges-yt:  python -I scripts/relatorio_decupagem.py [rev1|rev2] (cópia do script de Bruxelas)"""
import json
import os
import sys

REV = sys.argv[1] if len(sys.argv) > 1 else "rev1"

edl = json.load(open(f"{REV}/edl_{REV}.json"))
tr = json.load(open("_tmp/transcricao.json"))
dec = json.load(open(f"{REV}/decisoes_{REV}.json"))
conf = {round(c["de"], 1): c for c in json.load(open("_tmp/confere_cortes.json"))} if os.path.exists("_tmp/confere_cortes.json") else {}
ws = sorted([w for s in tr["segmentos"] for w in s["palavras"]], key=lambda w: w["ini"])


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def ms_(t):
    return f"{int(t // 60)}:{t % 60:04.1f}".replace(".", ",")


L = [f"# {REV.upper()} · Decupagem da voz (vlog de Bruges)", "",
     f"Fonte: `fonte/1120.mp4` (14:43,5). Feita por `scripts/decupar.py` (pausas pela energia da voz, sem corte sobre começo de palavra) + `scripts/hesitacoes.py` (\"ééé\", \"ahn\") + `scripts/prolongamentos.py` (palavra curta esticada: \"e…\", \"aí…\", \"já…\") + os cortes manuais de `{REV}/decisoes_{REV}.json`. Tudo em quadros inteiros (24 fps): imagem e som cortam juntos.", "",
     f"**Resultado:** 14:43,5 → **{ms_(edl['duracao_saida_s'])}** (−{edl['removido_s']:.1f} s em {len(edl['removidos'])} cortes)".replace(".", ",") + ". A compra do bilhete (0:00–0:09,75) sai do começo e vira o fim do gancho (4,5 s).", "",
     "## Como foi decidido (seu pedido de 20/11/2026)", "",
     "- **\"Não deixe espaço entre minhas vozes\":** toda pausa com mais de 0,32 s entre palavras sai; ficam 0,12 s depois da palavra e 0,08 s antes da próxima (em Bruxelas eram 0,18 e 0,12: aqui a fala fica mais corrida, como pede o padrão de edição de 19/11). Pausa com corte de cena dentro: apara o fim de um plano e o começo do outro, deixando ≥ 0,5 s de cada.",
     "- **\"Corte quando eu prolongo muito na fala\":** palavra curta (até 4 letras) com mais de 0,6 s e mais de 2,2 vezes a duração normal: o arrasto foi transcrito de novo sozinho; se não tinha palavra de verdade dentro, sai (a palavra fica, com os primeiros 0,25 s). Palavra longa esticada (\"carruagem\", \"trigésima\") fica: cortar no meio pode comer sílaba.",
     "- **Hesitação (\"ééé\", \"ahn\"):** só sai onde a 2ª transcrição ESCREVEU a hesitação. Em trecho curto o Whisper inventa texto (\"Obrigado\", \"Tchau\"): nesses casos o trecho ficou, para não arriscar comer palavra.",
     "- **Tropeço no nome:** \"o Alferia, acho que fala assim,\" antes de \"Chez Albert\" (1:19) saiu: fica \"um dos pontos turísticos da cidade, Chez Albert\".",
     "- **Não mexi:** nas montagens de paisagem (onde entra a música), na pausa da Marina em \"pela trigésima… sétima vez\" (é a piada) e no time-lapse (vira 4× mais rápido, pedido seu).", "",
     "**A transcrição é automática e o Claude não escuta áudio.** Na prévia, confira se algum corte ficou seco ou se sobrou algum prolongamento: me passe o minuto e eu ajusto.", "",
     "## Cortes (minutos da fonte)", "", "| Fonte | Sai | Motivo | Antes ‖ depois |", "|---|---:|---|---|"]
for r in edl["removidos"]:
    a = r["de_s"]
    b = a + r["dur_s"]
    antes = [w["p"] for w in ws if w["fim"] <= a + 0.05][-3:]
    depois = [w["p"] for w in ws if w["ini"] >= b - 0.05][:3]
    dentro = [w["p"] for w in ws if w["ini"] < b - 0.02 and w["fim"] > a + 0.02]
    L.append(f"| {mmss(a)} | {r['dur_s']:.2f} s | {r['motivo']} | …{' '.join(antes)} ‖ {' '.join(depois)}… |")
L += ["", "## Trechos protegidos ou que pareciam vazios e ficaram", "", "| Fonte | Por quê |", "|---|---|"]
for n in dec.get("zonas_protegidas", []) + dec.get("nao_cortados", []):
    L.append(f"| {mmss(n['de'])}–{mmss(n['ate'])} | {n['motivo']} |")
if dec.get("congelar"):
    L += ["", "## Quadros congelados (a imagem para, o som segue)", "", "| Fonte | Por quê |", "|---|---|"]
    for n in dec["congelar"]:
        L.append(f"| {mmss(n['de'])}–{mmss(n['ate'])} | {n['motivo']} |")
open(f"{REV}/DECUPAGEM_{REV.upper()}.md", "w").write("\n".join(L) + "\n")
print(len(edl["removidos"]), "cortes")
