"""Baixa as imagens do Commons listadas em <pasta>/lista.json (chave → título) e guarda licença e autor em meta.json.

Uma consulta à API para todos os títulos (URL, tamanho e metadados) e download sequencial com pausa (o Commons limita
pedidos seguidos: HTTP 429). Imagem pelo thumb.php do Commons, até 1920 px de largura.
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
UA = {"User-Agent": "PrimeiroDiaReel/1.0 (reel_gaudi; Wikimedia Commons image credits)"}


def get(url, tent=8):
    for k in range(tent):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            espera = min(int(e.headers.get("Retry-After") or 0) or 10 * (k + 1), 60)
            print(f"   429 · {espera} s", file=sys.stderr, flush=True)
            time.sleep(espera)
    raise RuntimeError("limite de acesso")


def main():
    pasta = sys.argv[1]
    lista = json.load(open(os.path.join(pasta, "lista.json"), encoding="utf-8"))
    arq = os.path.join(pasta, "meta.json")
    meta = json.load(open(arq, encoding="utf-8")) if os.path.exists(arq) else {}
    falta = {k: t for k, t in lista.items() if not (k in meta and os.path.exists(os.path.join(pasta, f"{k}.jpg")) and os.path.getsize(os.path.join(pasta, f"{k}.jpg")) > 1000)}
    titulos = list(falta.values())
    info = {}
    for i in range(0, len(titulos), 20):
        q = urllib.parse.urlencode(dict(action="query", titles="|".join(titulos[i:i + 20]), prop="imageinfo|categories", iiprop="url|size|extmetadata",
                                        iiurlwidth=1920, cllimit=100, format="json"))
        r = json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))
        norm = {n["to"]: n["from"] for n in r["query"].get("normalized", [])}
        for pg in r["query"]["pages"].values():
            info[norm.get(pg["title"], pg["title"])] = pg
    for k, t in falta.items():
        pg = info.get(t)
        if not pg or "imageinfo" not in pg:
            print(k, "NÃO ENCONTRADO", t, flush=True)
            continue
        ii = pg["imageinfo"][0]
        # thumb.php do próprio Commons (o upload.wikimedia.org pede 600 s entre pedidos deste IP)
        nome = urllib.parse.quote(t.split(":", 1)[1].replace(" ", "_"))
        url = f"https://commons.wikimedia.org/w/thumb.php?f={nome}&w={min(ii['width'], 1920)}"
        time.sleep(3)
        try:
            dados = get(url)
        except Exception as e:
            print(k, "ERRO", e, flush=True)
            continue
        if len(dados) < 1000 or dados[:2] != b"\xff\xd8":
            print(k, "ERRO resposta vazia ou não é JPEG", flush=True)  # o Commons às vezes responde 200 vazio sob limite
            continue
        open(os.path.join(pasta, f"{k}.jpg"), "wb").write(dados)
        m = ii.get("extmetadata", {})
        g = lambda c: re.sub(r"\s+", " ", re.sub("<[^>]+>", "", m.get(c, {}).get("value", ""))).strip()
        meta[k] = dict(titulo=t, pagina=ii["descriptionurl"], url=url, licenca=g("LicenseShortName"), autor=g("Artist"), data=g("DateTimeOriginal"),
                       credito=g("Credit"), descricao=g("ImageDescription")[:500], largura=ii["width"], altura=ii["height"],
                       categorias=[c["title"] for c in pg.get("categories", [])])
        json.dump(meta, open(arq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(k, "ok", meta[k]["licenca"], ii["width"], "x", ii["height"], flush=True)


if __name__ == "__main__":
    main()
