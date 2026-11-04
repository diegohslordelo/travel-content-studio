"""Contornos reais (Natural Earth 1:10m, domínio público) projetados para a caixa 1080 × 900 do mapa do gancho.
Saída: public/mapa.json (caminhos SVG de cada país + cidades). Uso: python3 scripts/mapa.py"""
import json, math
LON0, LAT0, K = 2.6, 51.45, 346.0
C = math.cos(math.radians(51.5))
def P(lon, lat):
    return (540 + (lon - LON0) * K * C, 450 - (lat - LAT0) * K)
def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / n
        if d > dmax: dmax, idx = d, i
    if dmax > eps:
        return dp(pts[: idx + 1], eps)[:-1] + dp(pts[idx:], eps)
    return [pts[0], pts[-1]]
g = json.load(open("mapa/ne10_admin.geojson"))
paises = {}
for f in g["features"]:
    iso = f["properties"].get("ADM0_A3")
    if iso not in ("FRA", "BEL", "NLD", "DEU", "LUX", "GBR"): continue
    geom = f["geometry"]; polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    d = []
    for poly in polys:
        for anel in poly[:1]:
            if not any(-3 < lo < 10 and 46 < la < 55 for lo, la in anel): continue
            pts = [P(lo, la) for lo, la in anel]
            h = len(pts) // 2  # anel fechado: simplifica as duas metades (o 1º e o último ponto coincidem)
            pts = dp(pts[: h + 1], 0.8)[:-1] + dp(pts[h:], 0.8)
            if len(pts) < 4: continue
            d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    paises[iso] = "".join(d)
cidades = {"Bruges": (3.2247, 51.2093), "Bruxelas": (4.3517, 50.8503), "Amsterdam": (4.9041, 52.3676), "Paris": (2.3522, 48.8566), "Gent": (3.7174, 51.0543)}
out = {"paises": paises, "cidades": {k: [round(v, 1) for v in P(*c)] for k, c in cidades.items()}, "proj": {"lon0": LON0, "lat0": LAT0, "k": K}}
json.dump(out, open("public/mapa.json", "w"))
print({k: len(v) for k, v in paises.items()}, out["cidades"])
