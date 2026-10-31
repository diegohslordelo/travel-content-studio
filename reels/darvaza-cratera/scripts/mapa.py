"""Gera o mapa do Reel (países do Natural Earth 1:50m, domínio público) em caminhos SVG já projetados.
Projeção equirretangular com cos(40°) no eixo x (a latitude de Darvaza), 1 grau de latitude = 10 unidades.
Uso: python3 scripts/mapa.py <ne_50m_admin_0_countries.geojson>  → mapa/paises.json"""
import json, math, sys
K = 10.0
CX = math.cos(math.radians(40))
DARVAZA = (58.4397, 40.2525)  # Wikipedia, "Darvaza gas crater" (40°15′09″N 58°26′22″E)

def proj(lon, lat):
    return (lon * K * CX, (90 - lat) * K)

def anel(coords):
    pts = [proj(lo, la) for lo, la in coords]
    out, ult = [], None
    for x, y in pts:
        p = (round(x, 1), round(y, 1))
        if p != ult: out.append(p); ult = p
    if len(out) < 3: return ""
    return "M" + "L".join(f"{x} {y}" for x, y in out) + "Z"

d = json.load(open(sys.argv[1]))
paises = []
for f in d["features"]:
    g = f["geometry"]; nome = f["properties"]["NAME"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    caminhos = []
    for poly in polys:
        lons = [c[0] for c in poly[0]]; lats = [c[1] for c in poly[0]]
        if max(lons) < -25 or min(lons) > 150 or max(lats) < -40 or min(lats) > 78: continue
        caminhos.append("".join(anel(r) for r in poly))
    if caminhos:
        paises.append({"nome": nome, "d": "".join(caminhos)})
dx, dy = proj(*DARVAZA)
json.dump({"paises": paises, "darvaza": [round(dx, 1), round(dy, 1)], "k": K, "cx": CX}, open("mapa/paises.json", "w"))
tk = next(p for p in paises if p["nome"] == "Turkmenistan")
print(len(paises), "países; Darvaza em", round(dx, 1), round(dy, 1))
