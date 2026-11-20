"""Mapa do trem Bruxelas → Bruges (DS V2 5.4, versão 2.3.0: mapa próprio em cores naturais, base OpenStreetMap).

Roda de reels/bruges-yt:  python -I scripts/mapa_trem.py
Escreve public/mapa_trem.json no formato do componente `MapaRota` (design-system/remotion/src/yt/Objetos16x9.tsx).

Base: tiles vetoriais oficiais do OpenStreetMap (esquema Shortbread, zoom 9), com cache em _tmp/mapa/tiles; funções de
`scripts/mapa_osm.py` (cópia do vlog de Bruxelas). Crédito "© OpenStreetMap contributors" na tela e na descrição.

Rota: curva suave pelas estações da linha 50A (Bruxelas-Central, Bruxelas-Sul, Denderleeuw, Gent-Sint-Pieters, Aalter,
Bruges). Nesta escala os trilhos do OSM chegam cortados nos tiles e o caminho mais curto desviava; a curva é o desenho do
trajeto (≈ 92 km), não o traçado exato do trilho nem o rastro do GPS.
Paradas: GPS dos clipes no acervo (acervo/bruges/indice.tsv): IMG_2417 às 09:44 na Bruxelas-Central (a compra do
bilhete) e IMG_2419 às 11:04 na estação de Bruges ("acabamos de chegar").
"""
import importlib.util
import math
import os

_spec = importlib.util.spec_from_file_location("mapa_osm", os.path.join(os.path.dirname(__file__), "mapa_osm.py"))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)

ESTACAO = {
    "bruxelas": (50.8455, 4.3570),  # Bruxelas-Central (GPS de IMG_2417, 09:44)
    "bruges": (51.1968, 3.2168),    # estação de Bruges (GPS de IMG_2419, 11:04)
    "gent": (51.0359, 3.7107),      # Gent-Sint-Pieters (OSM): ponto de passagem da linha Bruxelas–Bruges
}
# pontos de passagem da linha 50A (Bruxelas-Sul – Denderleeuw – Gent – Bruges), para o caminho não desviar
PASSAGEM = [(50.8357, 4.3363), (50.8913, 4.0727), (51.0359, 3.7107), (51.0868, 3.4466)]  # Bruxelas-Sul, Denderleeuw, Gent-Sint-Pieters, Aalter
m.LUGAR.update(ESTACAO)


def catmull_rom(pts, passos=24):
    """Curva suave que passa por todos os pontos (Catmull-Rom centrípeta simplificada, uniforme)."""
    ext = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for k in range(passos):
            t = k / passos
            out.append(tuple(
                0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3)
                for j in (0, 1)
            ))
    out.append(pts[-1])
    return out


def main():
    z = 9
    fs = m.feicoes(50.70, 2.90, 51.40, 4.60, z=z)
    # Nesta escala (≈ 67 m por pixel) os trilhos do OSM chegam cortados nos tiles e o caminho mais curto desvia por
    # Mechelen ou Kortrijk. A Rota é uma curva suave pelas estações da linha 50A (Bruxelas-Sul, Denderleeuw,
    # Gent-Sint-Pieters, Aalter): o desenho do trajeto, não o traçado exato do trilho.
    pts = [m.merc(*p) for p in [ESTACAO["bruxelas"]] + PASSAGEM + [ESTACAO["bruges"]]]
    r = catmull_rom(pts)
    lat_c = (ESTACAO["bruxelas"][0] + ESTACAO["bruges"][0]) / 2 + 0.01
    lon_c = (ESTACAO["bruxelas"][1] + ESTACAO["bruges"][1]) / 2
    pj = m.Projecao(lat_c, lon_c, 128000)
    b = m.base(fs, pj, com_minor=False)
    # nesta escala os riachos e canais pequenos viram um emaranhado azul: ficam só os rios e canais longos (≥ 60 px)
    b["canal"] = []
    for camada, pr, t, partes in fs:
        if camada == "water_lines" and pr.get("kind") in {"river", "canal"}:
            for l in partes:
                pts = [pj.xy(p) for p in l]
                comp = sum(math.dist(u, v) for u, v in zip(pts, pts[1:]))
                if comp >= 60 and m.dentro(pts) and (c := m.caminho(pts, tol=2.5)):
                    b["canal"].append(c)
    b["parque"] = [c for c in b["parque"] if len(c) > 400]  # só as manchas verdes grandes
    # nesta escala, só as vias principais (as secundárias viram um emaranhado) e o mar do Norte
    b["major"] = []
    for camada, pr, t, partes in fs:
        if camada == "streets" and pr.get("kind") in {"motorway", "trunk"} and not pr.get("tunnel"):
            for l in partes:
                pts = [pj.xy(p) for p in l]
                if m.dentro(pts, 200) and (c := m.caminho(pts, tol=2.5)):
                    b["major"].append(c)
        elif camada == "ocean":
            for anel in partes:
                pts = [pj.xy(p) for p in anel]
                if m.dentro(pts) and (c := m.caminho(pts, True, tol=2.5)):
                    b["agua"].append(c)
    km = sum(
        math.dist(a, c) * 40075016.686 * math.cos(math.radians(lat_c)) / 1000 for a, c in zip(r, r[1:])
    )
    print(f"trilho desenhado: {km:.0f} km")
    m.salva("trem", b, pj, r, [("bruxelas", "BRUXELAS", "09H44", (-300, 34)), ("bruges", "BRUGES", "11H04", (-250, 40))])


if __name__ == "__main__":
    main()
