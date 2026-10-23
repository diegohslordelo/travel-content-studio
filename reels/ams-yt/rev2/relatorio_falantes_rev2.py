"""Relatório de quem fala (REV2), a partir de `_tmp/falantes.json` (`scripts/quem_fala.py`): o resumo, as falas que
viraram texto, narração ou decisão do vídeo, e a lista completa de frases da Marina e de dúvida, no relógio do
vídeo final da REV2.

Roda de reels/ams-yt:  python rev2/relatorio_falantes_rev2.py  →  rev2/FALANTES_REV2.md
"""
import json
import sys

sys.path.insert(0, "rev2")
import montar_rev2 as mt  # noqa: E402

# falas que importam para o vídeo: (trecho da fonte em s, por que importa)
CHAVE = [
    (211.8, "Fala real no gancho (\"Gente, meu cabelo!\")"),
    (220.2, "Exemplo da alternativa B do gancho (\"eu sei que não vai chover\")"),
    (227.7, "Resposta logo depois"),
    (316.6, "Base do F1 da narração (\"fica encantado com cada rua\")"),
    (360.4, "\"Casinha bonitinha\" (usada na proposta do desfecho)"),
    (367.0, "\"As casinhas aqui são muito bonitinhas\""),
    (807.9, "O \"Não\" do McCrispy (rufar e confete)"),
    (936.6, "\"Fica a dica aí\" (Anne Frank)"),
    (941.9, "\"Vale cada centavo\" (Anne Frank)"),
    (1160.4, "\"Surreal\" do stroopwafel"),
    (1837.8, "\"Vale muito a pena também\" (Heineken)"),
    (1864.2, "\"Esse daqui bebeu quatro\""),
    (1865.6, "Fala real no gancho (\"Bebi quatro\")"),
    (1876.1, "\"Valeu muito a pena\": selo VALE A PENA"),
    (1926.0, "2º FEBO (recibo novo)"),
    (1939.9, "Focaccia (recibo novo)"),
    (1961.0, "\"Estou empolgada\": última fala antes do fechamento"),
]


def mmss(ms):
    return f"{int(ms // 60000):02d}:{(ms % 60000) / 1000:04.1f}"


def main():
    d = json.load(open("_tmp/falantes.json", encoding="utf-8"))
    edl = json.load(open("rev1/edl_rev1.json", encoding="utf-8"))
    lt = json.load(open("rev2/linha_do_tempo_rev2.json", encoding="utf-8"))
    mp = mt.Mapa(edl, lt["gancho_ms"])
    manter = [(a / 24, b / 24) for a, b in edl["manter"]]

    def no_video(t):
        return any(a <= t < b for a, b in manter)

    def marcado(f):
        return " ".join(f"{w['p']}" + ("" if w["quem"] == "?" else f"/{w['quem']}") for w in f["palavras"])

    fr = d["frases"]
    cont = {}
    for f in fr:
        cont[f["quem"]] = cont.get(f["quem"], 0) + 1
    L = ["# REV2 · Quem fala (medição pelo tom de voz)", "",
         "Pedido do Diego (23/10/2026): separar as falas dele das da Marina pelo tom de voz. Script: `scripts/quem_fala.py`. **É medição, não escuta**: confirme ouvindo as frases marcadas como dúvida.", "",
         "## Como foi medido", "",
         f"- Frequência fundamental (F0, pYIN) de cada palavra da transcrição (Whisper large-v3 da fonte).",
         f"- Referências medidas: as suas narrações de 22/10 (só você): mediana **{d['ref_diego_hz']:.0f} Hz**; trechos em que só a Marina fala e a imagem confirma (\"Surreal\" e \"Tomara que não, porque nem guarda-chuva eu tenho\"): **{d['ref_marina_hz']:.0f} Hz**.",
         f"- As palavras do vídeo inteiro formam dois grupos: em volta de **{d['gmm_hz'][0]:.0f} Hz** ({d['gmm_peso'][0]:.0%} das palavras) e de **{d['gmm_hz'][1]:.0f} Hz** ({d['gmm_peso'][1]:.0%}). O limiar entre eles é **{d['limiar_hz']:.0f} Hz**; a menos de {str(d['margem_semitons']).replace('.', ',')} semitom do limiar a palavra fica como dúvida.",
         "- Limites: risada, grito e animação sobem a sua voz; vento e sílabas curtas fazem o pYIN errar a oitava. Uma frase com palavras dos dois lados pode ser troca de quem fala ou erro de medida.", "",
         f"Resultado: {cont.get('Diego', 0)} frases suas, {cont.get('Marina', 0)} da Marina, {cont.get('dúvida', 0)} com dúvida (as duas vozes ou medida no limite) e {cont.get('sem voz medida', 0)} sem voz medida (curtas demais ou só ruído).", "",
         "## As falas que importam para o vídeo", "", "| Vídeo final | Fonte | Quem (medido) | F0 | Frase, palavra a palavra (D = Diego, M = Marina) | Por que importa |", "|---|---|---|---:|---|---|"]
    for t, porque in CHAVE:
        f = min(fr, key=lambda x: abs(x["ini"] - t))
        onde = mmss(mp.ms(f["ini"])) if no_video(f["ini"] + 0.2) else "fora do corpo"
        L.append(f"| {onde} | {mmss(f['ini'] * 1000)} | {f['quem']} | {f['f0'] or '—'} | {marcado(f)} | {porque} |")
    L += ["", "**No gancho**: \"Bebi quatro, estou realizado\" é seu (144–157 Hz). \"Gente, meu cabelo!\" saiu misturado: \"Gente\" mediu na sua faixa e \"meu cabelo\" na da Marina; com o vento dessa cena a medida não decide. Ouça esse trecho (00:03 do vídeo final). Ele entra como fala real, sem nome na tela, então não muda a montagem.", "",
          "**A pergunta do resumo** (\"quem disse 'eu sei que não vai chover'?\"): você (140 Hz). A Marina responde em seguida: \"Tomara que não, porque nem guarda-chuva eu tenho\" (293 Hz).", "",
          "## Na legenda (.srt)", "",
          "Uma legenda nunca junta a sua fala e a da Marina: a troca de quem fala abre legenda nova. Não pus o nome (\"Marina: …\"): o DS V2 (3.4.1) só pede o nome quando a pessoa não aparece, e a medição de voz não sabe se ela aparece.", "",
          "## Frases da Marina no vídeo", "", "| Vídeo final | Fonte | F0 | Frase |", "|---|---|---:|---|"]
    for f in fr:
        if f["quem"] == "Marina" and no_video(f["ini"] + 0.2):
            L.append(f"| {mmss(mp.ms(f['ini']))} | {mmss(f['ini'] * 1000)} | {f['f0']} | {f['texto']} |")
    L += ["", "## Frases com dúvida (ouvir)", "", "| Vídeo final | Fonte | F0 | Frase, palavra a palavra |", "|---|---|---:|---|"]
    for f in fr:
        if f["quem"] == "dúvida" and no_video(f["ini"] + 0.2):
            L.append(f"| {mmss(mp.ms(f['ini']))} | {mmss(f['ini'] * 1000)} | {f['f0']} | {marcado(f)} |")
    open("rev2/FALANTES_REV2.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("ok", cont)


if __name__ == "__main__":
    main()
