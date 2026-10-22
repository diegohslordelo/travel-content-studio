#!/usr/bin/env python3
"""Mapa da Europa do Reel greves-europa · REV1.

Converte o TopoJSON do Natural Earth 1:50m (pacote npm `world-atlas@2.0.2`, domínio público; licença ISC
do empacotamento) em caminhos SVG já projetados (Mercator), num plano de 4000 px de largura.
Saída: assets/mapa_europa.json (lido pela composição `ReelGreves`).

    python3 mapa_europa.py caminho/countries-50m.json

Download: https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-50m.json
"""
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "assets", "mapa_europa.json")

# janela do plano: longitude −25 a 45, latitude 27 a 66
LON0, LON1 = -25.0, 45.0
LAT0, LAT1 = 27.0, 66.0
LARGURA = 4000.0

# países com papel no vídeo (ISO 3166 numérico, como no world-atlas)
DESTAQUES = {"380": "ITA", "250": "FRA", "724": "ESP", "056": "BEL", "620": "PRT"}


def merc_y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


ESCALA = LARGURA / math.radians(LON1 - LON0)
Y_TOPO = merc_y(LAT1)
ALTURA = (Y_TOPO - merc_y(LAT0)) * ESCALA


def projetar(lon, lat):
    x = math.radians(lon - LON0) * ESCALA
    y = (Y_TOPO - merc_y(max(min(lat, 85), -85))) * ESCALA
    return x, y


def decodificar_arcos(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcos = []
    for arco in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arco:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcos.append(pts)
    return arcos


def anel(indices, arcos):
    pts = []
    for i in indices:
        a = arcos[i] if i >= 0 else list(reversed(arcos[~i]))
        pts.extend(a if not pts else a[1:])
    return pts


def poligonos(geo):
    if geo["type"] == "Polygon":
        return [geo["arcs"]]
    if geo["type"] == "MultiPolygon":
        return geo["arcs"]
    return []


def main():
    topo = json.load(open(sys.argv[1], encoding="utf-8"))
    arcos = decodificar_arcos(topo)
    paises = []
    for g in topo["objects"]["countries"]["geometries"]:
        partes = []
        lons, lats = [], []
        for poly in poligonos(g):
            for indices in poly:
                pts = anel(indices, arcos)
                # descarta anéis fora da janela (ilhas distantes, territórios ultramarinos)
                if not any(LON0 - 5 < lo < LON1 + 5 and LAT0 - 5 < la < LAT1 + 5 for lo, la in pts):
                    continue
                lons += [p[0] for p in pts]
                lats += [p[1] for p in pts]
                xy = [projetar(lo, la) for lo, la in pts]
                d = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in xy) + "Z"
                partes.append(d)
        if not partes:
            continue
        paises.append({
            "id": g.get("id"),
            "nome": g["properties"]["name"],
            "codigo": DESTAQUES.get(g.get("id")),
            "d": "".join(partes),
        })
    def centro(lon, lat):
        x, y = projetar(lon, lat)
        return [round(x, 1), round(y, 1)]
    dados = {
        "fonte": "Natural Earth 1:50m via world-atlas@2.0.2 (domínio público)",
        "projecao": "Mercator",
        "largura": LARGURA,
        "altura": round(ALTURA, 1),
        "janela": {"lon": [LON0, LON1], "lat": [LAT0, LAT1]},
        # pontos de referência (lon, lat) projetados, para câmera e rótulos
        "pontos": {
            "italia": centro(12.6, 42.6),
            "franca": centro(2.4, 46.6),
            "espanha": centro(-3.6, 40.2),
            "portugal": centro(-8.1, 39.6),
            "iberia": centro(3.0, 43.6),
            "europa": centro(4.6, 44.5),
            "roma": centro(12.4964, 41.9028),
            "milao": centro(9.19, 45.4642),
            "paris": centro(2.3522, 48.8566),
            "madrid": centro(-3.7038, 40.4168),
        },
        "paises": paises,
    }
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(paises)} países · {os.path.getsize(SAIDA) / 1024:.0f} KB → {os.path.relpath(SAIDA, AQUI)}")


if __name__ == "__main__":
    main()
