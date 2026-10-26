"""Busca no Wikimedia Commons: título, tamanho, licença, autor e data (para escolher e creditar as imagens)."""
import json, sys, time, urllib.error, urllib.parse, urllib.request, re
UA = {"User-Agent": "PrimeiroDiaReel/1.0 (diegohslordelo; reel_gaudi)"}
def api(**p):
    p.update(format="json")
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
    for k in range(6):
        try:
            time.sleep(2)
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            espera = int(e.headers.get("Retry-After") or 0) or 15 * (k + 1)
            print(f"   (429: esperando {espera} s)", file=sys.stderr)
            time.sleep(espera)
    raise RuntimeError("Commons: limite de acesso")
def info(titulos):
    r = api(action="query", titles="|".join(titulos), prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1600)
    out = []
    for pg in r["query"]["pages"].values():
        if "imageinfo" not in pg: continue
        ii = pg["imageinfo"][0]; m = ii.get("extmetadata", {})
        g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", ""))[:90]
        out.append(dict(titulo=pg["title"], w=ii["width"], h=ii["height"], licenca=g("LicenseShortName"), autor=g("Artist"),
                        data=g("DateTimeOriginal"), url=ii["url"], thumb=ii.get("thumburl"), pagina=ii["descriptionurl"], desc=g("ImageDescription")))
    return out
if __name__ == "__main__":
    modo, q = sys.argv[1], " ".join(sys.argv[2:])
    if modo == "busca":
        r = api(action="query", list="search", srsearch=q, srnamespace=6, srlimit=25)
        tit = [x["title"] for x in r["query"]["search"]]
    else:
        r = api(action="query", list="categorymembers", cmtitle=q, cmtype="file", cmlimit=60)
        tit = [x["title"] for x in r["query"]["categorymembers"]]
    for i in range(0, len(tit), 20):
        for x in info(tit[i:i + 20]):
            print(f"{x['titulo'][5:80]:<75} {x['w']}x{x['h']} | {x['licenca']} | {x['autor'][:40]} | {x['data'][:20]}")


def baixar(titulo, destino, largura=1920):
    """Baixa a imagem (miniatura de até `largura` px, ou o original se for menor) e devolve os metadados."""
    r = api(action="query", titles=titulo, prop="imageinfo|categories", iiprop="url|size|extmetadata", iiurlwidth=largura, cllimit=50)
    pg = next(iter(r["query"]["pages"].values()))
    ii = pg["imageinfo"][0]
    # original até 3000 px; acima disso, a miniatura de 1920 px (tamanho padrão do Commons, já gerado em cache)
    url = ii["thumburl"] if ii["width"] > 3000 else ii["url"]
    dados = None
    for k in range(8):
        try:
            time.sleep(2)
            dados = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 0) or 20 * (k + 1))
    if dados is None:
        raise RuntimeError("Commons: limite de acesso no download")
    open(destino, "wb").write(dados)
    m = ii.get("extmetadata", {})
    g = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
    return dict(titulo=titulo, pagina=ii["descriptionurl"], licenca=g("LicenseShortName"), autor=g("Artist"), data=g("DateTimeOriginal"),
                credito=g("Credit"), descricao=g("ImageDescription")[:400], largura=ii["width"], altura=ii["height"],
                categorias=[c["title"] for c in pg.get("categories", [])])
