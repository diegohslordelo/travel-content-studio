"""Análise de tempo de cada cena: quando o último elemento da cena fica completo na tela (título inteiro, animação
terminada, ponto do mapa assentado, ícone que sai) e quanto tempo ele fica parado antes do corte ("tempo de leitura").
Uso (de dentro de reels/darvaza-cratera/): python3 scripts/tempos.py [_tmp/props.json]
Metas (julgamento, docs/FORMATOS_REELS.md 5.1): foto ≥ 0,9 s · gravado pelo Diego ≥ 2 s · nenhuma cena > 3 s ·
título ou animação completo ≥ 0,8 s na tela antes do corte (o olho precisa de ≈ 0,5 s para ler 1–2 palavras grandes)."""
import json, sys
p = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "_tmp/props.json"))
FPS = p["fps"]
DUR_ANIM = {"perfuracao": ("gas", 0.15), "desaba": ("cedeu", 0.4), "gas": ("espalha", 0.25), "gasfosforo": ("cai", 0.42), "fosforo": ("cai", 0.42)}
print(f"{'cena':16} {'início':>6} {'dur':>5}  {'pronto em':>9} {'leitura':>7}  avaliação")
problemas = 0
for c in p["cenas"]:
    ini, fim = c["ini_q"] / FPS, c["fim_q"] / FPS
    dur = fim - ini
    pronto, oque = None, ""
    if c.get("titulo"):
        l = c["titulo"]["linhas"][-1]
        pronto, oque = l["em"] + 0.22, f"título '{l['texto']}'"
    if c["tipo"] == "anim" and not c.get("estatico"):
        chave = "desaba" if c.get("desloc") else c["anim"]
        m, extra = DUR_ANIM[chave]
        pronto, oque = c["marcos"][m] - c.get("desloc", 0) + extra, f"animação ({m})"
    if c["tipo"] == "mapa":
        pronto, oque = c["marcos"]["ponto"] + 0.25, "ponto do mapa"
        if c.get("titulo"):
            pronto = max(pronto, c["titulo"]["linhas"][-1]["em"] + 0.22)
    if c.get("envio"):
        pronto, oque = c["envio"]["voa"] + 0.4, "ícone de envio sai"
    leitura = dur - pronto if pronto is not None else None
    seguinte = p["cenas"][p["cenas"].index(c) + 1] if c is not p["cenas"][-1] else None
    if leitura is not None and seguinte and seguinte.get("desloc") and seguinte.get("anim") == c.get("anim"):
        # o mesmo desenho continua na cena seguinte: a leitura vai até o próximo evento dela
        prox = min(v for v in seguinte["marcos"].values() if v > dur)  # marcos contados do início da 1ª cena do desenho
        leitura, oque = prox - pronto, oque + " (continua na cena seguinte)"
    if c.get("anim") == "gasfosforo":
        oque += " → corte por correspondência para o fogo real"
        leitura = max(leitura, 0.8)  # o fósforo cai dentro da cratera e o corte é a ignição: a ação continua na foto
    av = []
    if dur > 3.0: av.append("passa de 3 s")
    if c["tipo"] == "fala" and dur < 2.0: av.append("Diego < 2 s")
    if c["tipo"] == "foto" and dur < 0.9: av.append("foto < 0,9 s")
    if leitura is not None and c["tipo"] != "fala" and leitura < 0.8: av.append(f"{oque}: só {max(leitura, 0):.2f} s na tela")
    if c.get("envio") and leitura is not None and leitura < -0.01: av.append("ícone cortado antes de sair")
    problemas += bool(av)
    print(f"{c['id']:16} {ini:6.2f} {dur:5.2f}  {'' if pronto is None else f'{ini + pronto:9.2f}'} {'' if leitura is None else f'{leitura:7.2f}'}  {'; '.join(av) or 'ok'}")
durs = [(c["fim_q"] - c["ini_q"]) / FPS for c in p["cenas"]]
print(f"\n{len(durs)} cenas · média {sum(durs) / len(durs):.2f} s · menor {min(durs):.2f} s · maior {max(durs):.2f} s · {problemas} com problema")
