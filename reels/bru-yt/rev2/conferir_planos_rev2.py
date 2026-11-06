"""Lista os planos do vídeo final da REV2 com menos de 1 s de tela (pedido do Diego, 06/11/2026). Plano = trecho entre
duas emendas (decupagem, take, quadro congelado) ou cortes de cena de verdade da fonte. As rajadas de "cortes" a cada
~0,17 s são panorâmicas (24 → 30 qps) e não contam. Roda de reels/bru-yt:  python rev2/conferir_planos_rev2.py"""
import json
import sys

sys.path.insert(0, "scripts")
from decupar import cortes_reais  # noqa: E402

p = json.load(open("rev2/props_rev2.json"))
reais = cortes_reais(json.load(open("_tmp/cenas.json"))["cortes"])
lim = {}
for tr in p["trechos"]:
    s0 = tr["src"] / 1000
    s1 = s0 + (tr["ate"] - tr["de"]) / 1000
    if tr["ate"] - tr["de"] < 1:
        continue
    lim.setdefault(round(tr["de"]), ("congelado" if tr.get("congela") else "emenda", s0))
    if not tr.get("congela"):
        for c in reais:
            if s0 + 0.02 < c < s1 - 0.02:
                lim.setdefault(round(tr["de"] + (c - s0) * 1000), ("corte de cena", c))
fim = round(p["duracao"] - 20000)
L = sorted(lim) + [fim]


def mmss(ms):
    d = int(round(ms / 100))
    return f"{d // 600}:{(d % 600) / 10:04.1f}"


curtos = [(a, b) for a, b in zip(L, L[1:]) if b - a < 1000]
print(f"{len(L) - 1} planos no vídeo (sem a tela final); {len(curtos)} com menos de 1 s:")
for a, b in curtos:
    tipo, src = lim[a]
    print(f"  {mmss(a)}  {b - a} ms  ({tipo}, fonte {src:.2f} s)")
