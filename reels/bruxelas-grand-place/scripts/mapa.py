"""Mapa do Reel: países do Natural Earth 1:50m (domínio público), já projetados em SVG (equirretangular).
Parte do mapa do Reel da cratera de Darvaza (branch claude/reel-darvaza-cratera, reels/darvaza-cratera/mapa/paises.json,
cos 40° no eixo x) e reprojeta só o eixo x para cos 50,85° (latitude de Bruxelas): x' = x · cos(50,85°) / cos(40°).
Mantém só a Europa ocidental (lon −12 a 30, lat 36 a 62). 1 grau de latitude = 10 unidades.
Uso: python3 scripts/mapa.py <paises.json do Darvaza>  → mapa/paises.json"""
import json, math, re, sys
d = json.load(open(sys.argv[1]))
K, CX0 = d["k"], d["cx"]
CX = math.cos(math.radians(50.85))
f = CX / CX0
BRUXELAS = (4.3517, 50.8467)  # Grand-Place: 50°50′48″N 4°21′9″E (Wikipedia, "Grand-Place")
lon = lambda x: x / (K * CX0)
lat = lambda y: 90 - y / K
paises = []
for p in d["paises"]:
    aneis = re.findall(r"M[^Z]*Z", p["d"])
    keep = []
    for a in aneis:
        pts = [tuple(map(float, q.split())) for q in a[1:-1].split("L")]
        los = [lon(x) for x, _ in pts]; las = [lat(y) for _, y in pts]
        if max(los) < -12 or min(los) > 30 or max(las) < 36 or min(las) > 62: continue
        keep.append("M" + "L".join(f"{round(x * f, 1)} {y}" for x, y in pts) + "Z")
    if keep: paises.append({"nome": p["nome"], "d": "".join(keep)})
bx, by = BRUXELAS[0] * K * CX, (90 - BRUXELAS[1]) * K
json.dump({"paises": paises, "ponto": [round(bx, 2), round(by, 2)], "k": K, "cx": CX}, open("mapa/paises.json", "w"))
print(len(paises), "países:", ", ".join(p["nome"] for p in paises)[:300]); print("Bruxelas em", round(bx, 2), round(by, 2))
