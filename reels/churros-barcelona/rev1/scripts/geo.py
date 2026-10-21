#!/usr/bin/env python3
"""Gera rev1/geo/mundo.json (contornos simplificados para o globo) a partir do Natural Earth 1:50m.

Uso (de dentro de rev1/):  python3 scripts/geo.py <ne_50m_admin_0_countries.geojson>
Fonte: https://github.com/nvkelso/natural-earth-vector (v5.1.2, domínio público).
Só entram os países do hemisfério que o globo mostra (Américas, Atlântico, Europa e África);
Brasil e Espanha vão marcados para o destaque.
"""
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 0.12  # graus: distância mínima entre pontos consecutivos


def simplificar(anel):
    out = [anel[0]]
    for p in anel[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= TOL:
            out.append(p)
    if len(out) < 4:
        return None
    return [[round(x, 2), round(y, 2)] for x, y in out]


def main(arq):
    d = json.load(open(arq, encoding="utf-8"))
    paises = []
    for f in d["features"]:
        iso = f["properties"]["ADM0_A3"]
        g = f["geometry"]
        polis = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        aneis = []
        for poli in polis:
            ext = poli[0]
            lons = [p[0] for p in ext]
            lats = [p[1] for p in ext]
            if max(lons) < -120 or min(lons) > 70 or max(lats) < -60:
                continue
            s = simplificar(ext)
            if s:
                aneis.append(s)
        if aneis:
            paises.append({"iso": iso, "aneis": aneis})
    os.makedirs(os.path.join(AQUI, "geo"), exist_ok=True)
    out = os.path.join(AQUI, "geo", "mundo.json")
    json.dump({"fonte": "Natural Earth 1:50m v5.1.2 (domínio público)", "paises": paises}, open(out, "w"), separators=(",", ":"))
    print(f"{len(paises)} países · {os.path.getsize(out) / 1024:.0f} KB → {out}")


if __name__ == "__main__":
    main(sys.argv[1])
