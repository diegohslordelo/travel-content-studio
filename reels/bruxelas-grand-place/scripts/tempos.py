"""Tempo de cada cena: duração na tela e quando o título fica completo ("tempo de leitura" antes do corte).
Uso (de dentro de reels/bruxelas-grand-place/): python3 scripts/tempos.py [_tmp/props.json]
Metas: toda imagem de 2 a 3 s na tela (pedido do Diego) · título completo ≥ 0,8 s na tela antes do corte.
A cena 'antes_depois' tem duas imagens (gravura e vídeo de hoje) ligadas pela cortina: mede cada uma até o meio da cortina."""
import json, sys
p = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "_tmp/props.json"))
FPS = p["fps"]
print(f"{'cena':20} {'início':>6} {'dur':>5}  {'leitura':>7}  avaliação")
probs, durs = 0, []
for c in p["cenas"]:
    ini, dur = c["ini_q"] / FPS, (c["fim_q"] - c["ini_q"]) / FPS
    partes = [dur]
    if c.get("comparar"):
        meio = (c["comparar"]["de"] + c["comparar"]["ate"]) / 2
        partes = [meio, dur - meio]
    leitura = None
    if c.get("titulo"):
        leitura = dur - (c["titulo"]["linhas"][-1]["em"] + 0.22)
    av = [f"imagem de {x:.2f} s fora de 2–3 s" for x in partes if x < 2.0 - 1e-6 or x > 3.0 + 1e-6]
    if leitura is not None and leitura < 0.8: av.append(f"título só {leitura:.2f} s completo")
    probs += bool(av); durs += partes
    print(f"{c['id']:20} {ini:6.2f} {dur:5.2f}  {'' if leitura is None else f'{leitura:7.2f}'}  {'; '.join(av) or 'ok'}")
print(f"\n{len(durs)} imagens · média {sum(durs) / len(durs):.2f} s · menor {min(durs):.2f} s · maior {max(durs):.2f} s · {probs} cena(s) com problema")
