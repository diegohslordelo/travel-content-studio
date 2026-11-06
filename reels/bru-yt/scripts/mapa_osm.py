"""Mapas do vlog de Bruxelas (DS V2 5.4, versão 2.3.0: mapa próprio em cores naturais, base OpenStreetMap).

Roda de reels/bru-yt:  python scripts/mapa_osm.py
Escreve public/mapa_<nome>.json no formato do componente `MapaRota` (design-system/remotion/src/yt/Objetos16x9.tsx):
  major, minor, agua, canal, parque (caminhos SVG em 1920 × 1080), rota (pontos) e paradas (n, nome, hora, xy).

Base: tiles vetoriais oficiais do OpenStreetMap (https://vector.openstreetmap.org, esquema Shortbread, zoom 14), com
cache em _tmp/mapa/tiles (o Overpass não responde nesta rede). Uso pontual, dentro da política de tiles vetoriais
(operations.osmfoundation.org/policies/vector). Crédito "© OpenStreetMap contributors" na tela (o componente põe) e na
descrição do vídeo.

Rotas:
  - a pé: caminho mais curto pelas ruas e calçadões do OSM (grafo das ruas do tile);
  - de metrô: caminho mais curto pelos túneis de metrô do OSM (kind = subway), da estação mais perto da origem à mais
    perto do destino, com o trecho a pé nas pontas. É o desenho do trajeto possível, não o rastro do GPS.
Paradas: coordenadas do GPS dos clipes no acervo (acervo/bruxelas/indice.tsv) ou do OSM (Nominatim), hora do arquivo.
"""
import gzip
import json
import math
import os
import time
import urllib.request

import mapbox_vector_tile
import networkx as nx

Z = 14
UA = {"User-Agent": "travel-content-studio-map/1.0 (vlog map, one-off)"}
CACHE = "_tmp/mapa/tiles"
W, H = 1920, 1080

# lugares (lat, lon): GPS do clipe no acervo quando existe; senão, o ponto do OSM
LUGAR = {
    "hotel": (50.84686, 4.35553),       # ibis Brussels off Grand Place (OSM)
    "atomium": (50.89492, 4.34138),     # Atomium (OSM)
    "zinneke": (50.84878, 4.34566),     # Het Zinneke, Rue des Chartreux (OSM)
    "fritland": (50.84741, 4.35063),    # Fritland, Rue Henri Maus (OSM; GPS IMG_2204 50.8477, 4.3508)
    "bourse": (50.84808, 4.34990),      # Bolsa (Bourse), fachada no Boulevard Anspach
    "grandplace": (50.84671, 4.35252),  # Grand-Place (OSM)
    "jeanneke": (50.84852, 4.35411),    # Jeanneke Pis, Impasse de la Fidélité (OSM)
    "gaufre": (50.84854, 4.35350),      # Le Roi de la Gaufre, Rue de la Fourche (OSM; GPS IMG_2230 50.8486, 4.3535)
    "galeries": (50.84819, 4.35513),    # Galeries Royales Saint-Hubert (OSM)
    "manneken": (50.84499, 4.34999),    # Manneken Pis (OSM; GPS IMG_2258 50.8450, 4.3499)
    "montdesarts": (50.84386, 4.35677), # Mont des Arts (OSM)
    "placeroyale": (50.84228, 4.35910), # Place Royale (OSM)
    "madeleine": (50.84494, 4.35521),   # Brasserie de la Madeleine (OSM; GPS IMG_2379 50.8450, 4.3555)
    "merveilleux": (50.84804, 4.35216), # Aux Merveilleux de Fred, Petite rue au Beurre (OSM; GPS IMG_2389 50.8482, 4.3521)
    "spago": (50.84865, 4.34790),       # Spago, Rue du Pont de la Carpe (OSM; GPS IMG_2410 50.8488, 4.3481)
}

MAJOR = {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"}
MINOR = {"residential", "unclassified", "living_street", "pedestrian", "service", "footway", "path", "steps", "track", "cycleway", "busway", "road"}
ANDAR = MAJOR | MINOR
VERDE = {"park", "forest", "grass", "meadow", "garden", "village_green", "cemetery", "recreation_ground", "golf_course", "playground", "wood", "heath", "scrub", "allotments"}


def merc(lat, lon):
    x = (lon + 180) / 360
    s = math.sin(math.radians(lat))
    y = 0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)
    return x, y


def tile_de(lat, lon, z):
    x, y = merc(lat, lon)
    return int(x * 2**z), int(y * 2**z)


def baixa(z, x, y):
    os.makedirs(CACHE, exist_ok=True)
    arq = f"{CACHE}/{z}_{x}_{y}.mvt"
    if not os.path.exists(arq):
        url = f"https://vector.openstreetmap.org/shortbread_v1/{z}/{x}/{y}.mvt"
        b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        open(arq, "wb").write(b)
        time.sleep(0.3)
    b = open(arq, "rb").read()
    try:
        b = gzip.decompress(b)
    except OSError:
        pass
    return mapbox_vector_tile.decode(b, default_options={"y_coord_down": True})


def feicoes(lat0, lon0, lat1, lon1, z=Z):
    """Feições (camada, propriedades, lista de anéis/linhas em mercator global) dos tiles que cobrem a caixa."""
    xa, ya = tile_de(lat1, lon0, z)
    xb, yb = tile_de(lat0, lon1, z)
    out = []
    for tx in range(min(xa, xb), max(xa, xb) + 1):
        for ty in range(min(ya, yb), max(ya, yb) + 1):
            d = baixa(z, tx, ty)
            for camada, v in d.items():
                ext = v["extent"]
                for f in v["features"]:
                    g = f["geometry"]
                    conv = lambda p, tx=tx, ty=ty, ext=ext: ((tx + p[0] / ext) / 2**z, (ty + p[1] / ext) / 2**z)  # noqa: E731
                    t = g["type"]
                    c = g["coordinates"]
                    if t == "LineString":
                        partes = [[conv(p) for p in c]]
                    elif t == "MultiLineString":
                        partes = [[conv(p) for p in l] for l in c]
                    elif t == "Polygon":
                        partes = [[conv(p) for p in r] for r in c]
                    elif t == "MultiPolygon":
                        partes = [[conv(p) for p in r] for poly in c for r in poly]
                    else:
                        continue
                    out.append((camada, f["properties"], t, partes))
    return out


class Projecao:
    """Mercator global → tela 1920 × 1080, centrada em (lat, lon), com `largura_m` metros na largura da tela."""

    def __init__(self, lat, lon, largura_m):
        self.cx, self.cy = merc(lat, lon)
        m_por_unidade = 40075016.686 * math.cos(math.radians(lat))
        self.s = W / (largura_m / m_por_unidade)

    def xy(self, p):
        return (W / 2 + (p[0] - self.cx) * self.s, H / 2 + (p[1] - self.cy) * self.s)

    def ll(self, lat, lon):
        return self.xy(merc(lat, lon))


def caminho(pts, fechar=False, tol=1.5):
    """Lista de pontos de tela → 'M x y L …', sem pontos a menos de `tol` px do anterior."""
    if len(pts) < 2:
        return None
    out = [pts[0]]
    for p in pts[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= tol:
            out.append(p)
    if len(out) < 2:
        return None
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in out)
    return d + ("Z" if fechar else "")


def miudo(pts, px=6):
    """Polígono menor que `px` na tela (some na escala do mapa): fica de fora."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return max(xs) - min(xs) < px and max(ys) - min(ys) < px


def dentro(pts, margem=500):
    return any(-margem <= x <= W + margem and -margem <= y <= H + margem for x, y in pts)


def grafo(fs, tipos, so_tunel=None):
    """Grafo das linhas (ruas ou metrô); nós = ponto arredondado (≈ 0,5 m), peso = distância."""
    G = nx.Graph()
    chave = lambda p: (round(p[0] * 8e7), round(p[1] * 8e7))  # noqa: E731
    for camada, pr, t, partes in fs:
        if camada != "streets" or pr.get("kind") not in tipos:
            continue
        if so_tunel is not None and bool(pr.get("tunnel")) != so_tunel:
            continue
        for l in partes:
            for a, b in zip(l, l[1:]):
                ka, kb = chave(a), chave(b)
                if ka != kb:
                    G.add_edge(ka, kb, w=math.hypot(a[0] - b[0], a[1] - b[1]))
    # costura as pontas cortadas na borda dos tiles (pontos a menos de ~3 m)
    nos = list(G.nodes)
    grade = {}
    for k in nos:
        grade.setdefault((k[0] // 240, k[1] // 240), []).append(k)
    for k in nos:
        if G.degree(k) != 1:
            continue
        gx, gy = k[0] // 240, k[1] // 240
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for o in grade.get((gx + dx, gy + dy), []):
                    if o != k and not G.has_edge(k, o) and math.hypot(k[0] - o[0], k[1] - o[1]) < 240:
                        G.add_edge(k, o, w=math.hypot(k[0] - o[0], k[1] - o[1]) / 8e7)
    return G


def mais_perto(G, p):
    k = (p[0] * 8e7, p[1] * 8e7)
    return min(G.nodes, key=lambda n: (n[0] - k[0]) ** 2 + (n[1] - k[1]) ** 2)


def rota(G, a, b):
    na, nb = mais_perto(G, merc(*a)), mais_perto(G, merc(*b))
    cam = nx.shortest_path(G, na, nb, weight="w")
    return [(n[0] / 8e7, n[1] / 8e7) for n in cam]


def base(fs, pj, com_minor=True):
    d = {"major": [], "minor": [], "agua": [], "canal": [], "parque": []}
    for camada, pr, t, partes in fs:
        k = pr.get("kind")
        if camada == "water_polygons":
            for r in partes:
                pts = [pj.xy(p) for p in r]
                if dentro(pts) and not miudo(pts) and (c := caminho(pts, True)):
                    d["agua"].append(c)
        elif camada == "water_lines" and k in {"canal", "river"}:
            for l in partes:
                pts = [pj.xy(p) for p in l]
                if dentro(pts) and (c := caminho(pts)):
                    d["canal"].append(c)
        elif camada == "land" and k in VERDE:
            for r in partes:
                pts = [pj.xy(p) for p in r]
                if dentro(pts) and not miudo(pts) and (c := caminho(pts, True)):
                    d["parque"].append(c)
        elif camada == "streets" and not pr.get("tunnel"):
            grupo = "major" if k in MAJOR else "minor" if (k in MINOR and com_minor) else None
            if grupo is None or k in {"service", "track", "path", "cycleway", "steps", "busway"}:
                continue
            for l in partes:
                pts = [pj.xy(p) for p in l]
                if dentro(pts, 200) and (c := caminho(pts)):
                    d[grupo].append(c)
    return d


def salva(nome, d, pj, pontos_rota, paradas):
    pts = []
    for p in pontos_rota:
        x, y = pj.xy(p)
        if not pts or math.hypot(x - pts[-1][0], y - pts[-1][1]) >= 2:
            pts.append((x, y))
    d = dict(d)
    d["rota"] = [[round(x, 1), round(y, 1)] for x, y in pts]
    d["paradas"] = []
    for i, par in enumerate(paradas):
        k, nm, h = par[:3]
        p_ = {"n": i + 1, "nome": nm, "hora": h, "xy": [round(c, 1) for c in pj.ll(*LUGAR[k])]}
        if len(par) > 3:
            p_["rotulo"] = list(par[3])
        d["paradas"].append(p_)
    os.makedirs("public", exist_ok=True)
    json.dump(d, open(f"public/mapa_{nome}.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"public/mapa_{nome}.json: {sum(len(d[k]) for k in ('major', 'minor', 'agua', 'canal', 'parque'))} caminhos, rota {len(pts)} pontos, "
          f"paradas {[(p['nome'], p['xy']) for p in d['paradas']]}")


def main():
    # ---------- cidade: centro → Atomium (metrô) e volta ----------
    fs_c = feicoes(50.836, 4.325, 50.903, 4.372)  # z14: túneis do metrô para a rota
    metro = grafo(fs_c, {"subway"}, so_tunel=None)
    fs_c13 = feicoes(50.826, 4.270, 50.915, 4.430, z=13)  # z13: base da cidade, mais larga
    # trecho de metrô entre as estações mais perto (o grafo do metrô liga as linhas pelos pontos em comum)
    ida = rota(metro, LUGAR["hotel"], LUGAR["atomium"])
    ida = [merc(*LUGAR["hotel"])] + ida + [merc(*LUGAR["atomium"])]
    lat_c = (LUGAR["hotel"][0] + LUGAR["atomium"][0]) / 2
    lon_c = (LUGAR["hotel"][1] + LUGAR["atomium"][1]) / 2
    pj = Projecao(lat_c, lon_c, 10500)
    bc = base(fs_c13, pj, com_minor=False)
    salva("centro_atomium", bc, pj, ida, [("hotel", "GRAND PLACE", "11H29", (34, -20)), ("atomium", "ATOMIUM", "12H16", (40, 20))])
    volta = rota(metro, LUGAR["atomium"], LUGAR["zinneke"])
    volta = [merc(*LUGAR["atomium"])] + volta + [merc(*LUGAR["zinneke"])]
    salva("atomium_zinneke", bc, pj, volta, [("atomium", "ATOMIUM", "12H19", (40, -20)), ("zinneke", "ZINNEKE PIS", "13H16", (-330, 20))])

    # ---------- centro: rota a pé do dia ----------
    fs = feicoes(50.838, 4.336, 50.855, 4.372)
    andar = grafo(fs, ANDAR, so_tunel=False)
    pj2 = Projecao(50.8457, 4.3528, 1750)
    b2 = base(fs, pj2)
    pj3 = Projecao(50.8436, 4.3545, 1250)
    b3 = base(fs, pj3)
    ordem = ["zinneke", "fritland", "grandplace", "jeanneke", "gaufre", "galeries", "manneken", "montdesarts", "placeroyale", "madeleine", "merveilleux", "spago"]
    trechos = {}
    for a, b in zip(ordem, ordem[1:]):
        trechos[(a, b)] = rota(andar, LUGAR[a], LUGAR[b])
    # Manneken Pis → Monte das Artes → Praça Real (a subida para o bairro real)
    r = trechos[("manneken", "montdesarts")] + trechos[("montdesarts", "placeroyale")][1:]
    salva("manneken_praca_real", b3, pj3, r, [("manneken", "MANNEKEN PIS", "16H12", (-60, -70)), ("montdesarts", "MONT DES ARTS", "16H33", (36, -64)), ("placeroyale", "PRAÇA REAL", "16H34", (40, 24))])
    # o dia inteiro no centro (fechamento)
    tudo = []
    for a, b in zip(ordem, ordem[1:]):
        tudo += trechos[(a, b)] if not tudo else trechos[(a, b)][1:]
    salva("dia_centro", b2, pj2, tudo, [
        ("zinneke", "ZINNEKE", "13H16", (-250, -70)), ("fritland", "FRITLAND", "13H53", (-120, 34)), ("grandplace", "GRAND PLACE", "14H13", (-300, 40)),
        ("galeries", "GALERIAS", "14H49", (34, 10)), ("manneken", "MANNEKEN PIS", "16H12", (-330, 10)), ("placeroyale", "PRAÇA REAL", "16H34", (36, 20)),
        ("madeleine", "MADELEINE", "17H57", (34, -10)), ("merveilleux", "MERVEILLEUX", "18H38", (-60, -120)), ("spago", "SPAGO", "20H27", (-230, 24)),
    ])


if __name__ == "__main__":
    main()
