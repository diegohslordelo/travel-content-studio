"""Relatório da decupagem (revN/DECUPAGEM_REVN.md) a partir de revN/edl_revN.json, da transcrição e das decisões.
Roda de reels/bru-yt:  python scripts/relatorio_decupagem.py [rev1|rev2]"""
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


n_pausa = sum(1 for r in edl["removidos"] if r["motivo"].startswith("pausa") or "parado" in r["motivo"])
L = [f"# {REV.upper()} · Decupagem (vlog de Bruxelas)", "",
     f"Fonte: `fonte/1103_fala.mp4` (14:27,3). Feita por `scripts/decupar.py` (pausas pela energia da voz, sem corte sobre começo de palavra) + `scripts/hesitacoes.py` (hesitações) + os cortes manuais de `{REV}/decisoes_{REV}.json`; conferida por `scripts/confere_cortes.py`. Tudo em quadros inteiros (30 fps): imagem e som cortam juntos.", "",
     f"**Resultado:** 14:27,3 → **{ms_(edl['duracao_saida_s'])}** (−{edl['removido_s']:.1f} s em {len(edl['removidos'])} cortes)".replace(".", ",") + ". O corpo do vídeo vai até 14:22,2 da fonte; os \"cortes finais\" (Grand Place à noite, 14:22–14:27) abrem o fechamento.", "",
     "## Como foi decidido", "",
     "- **Pausa na fala:** silêncio entre palavras com mais de 0,42 s; ficam 0,18 s depois da palavra e 0,12 s antes da próxima. Pausa com corte de cena dentro: apara o fim de um plano e o começo do outro, deixando ≥ 0,5 s de cada.",
     "- **Hesitação (\"eee\"):** procurei voz entre as palavras e palavras \"é/e\" esticadas; cada candidato foi transcrito de novo sozinho. Só cortei onde a 2ª transcrição **escreveu** a hesitação (\"Ééé…\", \"E…\"): 2 casos, encurtados (a palavra fica, sai o arrasto). Os outros 14 candidatos ficaram: em trecho curto o Whisper inventa texto, e a regra é não arriscar comer palavra.",
     "- **Momento vazio longo:** 3 cortes manuais (mastigação e risada), conferidos com uma 2ª transcrição do trecho. Ficou de fora a Marina provando o merveilleux (12:13–12:22): parecia vazio, mas tem \"Nossa!\" e \"Caramba.\" no meio.",
     "- **Palavra que atravessa o corte:** o Whisper estica o fim da palavra sobre a pausa (ex.: \"metrô\", \"cristal\"). Nesses cortes, o áudio já cortado foi transcrito de novo: a palavra continua inteira (coluna \"Conferido\"). O único caso duvidoso (0,10 s dentro do \"sério\", 2:45) virou trecho protegido.",
     *([f"- **REV2 (pedido do Diego: planos com menos de 1 s e transições falhas):** nenhum pedaço com menos de 1 s entre dois cortes, ou entre um corte e uma troca de cena (as rajadas de \"cortes\" a cada 0,17 s são panorâmicas e não contam); 3 cortes de quadros com a câmera virando; 3 quadros congelados onde a câmera vira com a fala já começando. Ajustes automáticos: " + "; ".join(edl.get("fragmentos", []))] if REV != "rev1" else []),
     "- **Não mexi:** nas montagens com música (são a sua edição), na revelação do Zinneke (a pausa entre \"Ponto turístico de Bruxelas.\" e \"Um cachorro mijando.\" é a piada) e nas mordidas do waffle (montagem sua, com 3 cortes).", "",
     "**A transcrição é automática e o Claude não escuta áudio.** Na prévia, confira se algum corte ficou seco ou se sobrou algum \"eee\": me passe o minuto e eu ajusto.", "",
     "## Cortes (minutos da fonte)", "", "| Fonte | Sai | Motivo | Antes ‖ depois | Conferido |", "|---|---:|---|---|---|"]
for r in edl["removidos"]:
    a = r["de_s"]
    b = a + r["dur_s"]
    antes = [w["p"] for w in ws if w["fim"] <= a + 0.05][-3:]
    depois = [w["p"] for w in ws if w["ini"] >= b - 0.05][:3]
    dentro = [w["p"] for w in ws if w["ini"] < b - 0.02 and w["fim"] > a + 0.02]
    c = conf.get(round(a, 1))
    ok = (f"\"{' '.join(dentro)}\" inteira: «{c['depois_do_corte']}»" if c and c["palavra_inteira"] else f"conferir: «{c['depois_do_corte']}»" if c else "") if dentro else ""
    L.append(f"| {mmss(a)} | {r['dur_s']:.2f} s | {r['motivo']} | …{' '.join(antes)} ‖ {' '.join(depois)}… | {ok} |")
L += ["", "## Trechos protegidos ou que pareciam vazios e ficaram", "", "| Fonte | Por quê |", "|---|---|"]
for n in dec.get("zonas_protegidas", []) + dec.get("nao_cortados", []):
    L.append(f"| {mmss(n['de'])}–{mmss(n['ate'])} | {n['motivo']} |")
if dec.get("congelar"):
    L += ["", "## Quadros congelados (a imagem para, o som segue)", "", "| Fonte | Por quê |", "|---|---|"]
    for n in dec["congelar"]:
        L.append(f"| {mmss(n['de'])}–{mmss(n['ate'])} | {n['motivo']} |")
open(f"{REV}/DECUPAGEM_{REV.upper()}.md", "w").write("\n".join(L) + "\n")
print(len(edl["removidos"]), "cortes")
