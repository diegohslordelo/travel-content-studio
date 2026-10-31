"""Baixa do Wikimedia Commons as imagens históricas do Reel (thumb.php, com pausa e nova tentativa no 429) e guarda a
licença, o autor e a data de cada uma em imagens/lista_commons.json.
Uso (de dentro de reels/bruxelas-grand-place/): python3 scripts/baixar_imagens.py"""
import json, os, re, time, urllib.parse, urllib.request, urllib.error
UA = {"User-Agent": "PrimeiroDiaReel/1.0 (https://instagram.com/primeirodiaem; diegohs.lordelo@gmail.com) python-urllib"}
FOTOS = {
    "incendio": ("NIND MVB-Bombardement ISO200.jpg", 2400, "Pintura 'O bombardeio da Grand-Place em 1695' (anônimo, fim do séc. XVII), Museu da Cidade de Bruxelas; foto de Benoit Brummer"),
    "plano_bombardeio": ("Plattegrond van het bombardement van Brussel door de Fransen, 1695, Harmanus van Loon, Nicolas de Fer, Lodewijk XIV (koning van Frankrijk), 1695.jpg", 3200, "Plano do bombardeio de Bruxelas pelo exército francês, 13–15 de agosto de 1695 (Nicolas de Fer / Harmanus van Loon)"),
    "ruinas_coppens": ("Augustin Coppens, Grote Markt na bombardement.JPG", 1405, "Augustin Coppens, a Grand-Place depois do bombardeio (1695), desenho"),
    "ruinas_gravura": ("Ruïnes op de Grote Markt te Brussel, 1695 Bouvalligheden van de eene sijde van de Groote Merkt van de hoek van de Heuvelstraat naar S. Niklaas Ruinae a latere Fori Maximi nempe a Via Collina versus Fanum D. Nicolai (tit, RP-P-1921-449.jpg", 3200, "Ruínas de um lado da Grand-Place em 1695 (gravura segundo Augustin Coppens), Rijksmuseum"),
}
def get(u):
    for k in range(12):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(min(90, int(e.headers.get("retry-after") or 0) or 15 * (k + 1)))
    raise SystemExit("429 persistente")
api = lambda **p: json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(p, format="json"))))
d = api(action="query", titles="|".join("File:" + v[0] for v in FOTOS.values()), prop="imageinfo", iiprop="extmetadata|size")
meta = {}
for p in d["query"]["pages"].values():
    em = p["imageinfo"][0]["extmetadata"]; g = lambda k: re.sub("<[^>]+>", "", em.get(k, {}).get("value", "")).strip()
    meta[p["title"]] = {"autor": g("Artist"), "licenca": g("LicenseShortName"), "data": g("DateTimeOriginal"), "credito": g("Credit")[:200]}
lista = {}
for chave, (nome, w, desc) in FOTOS.items():
    out = f"imagens/commons/{chave}.jpg"
    if not (os.path.exists(out) and os.path.getsize(out) > 20000):
        b = get("https://commons.wikimedia.org/w/thumb.php?" + urllib.parse.urlencode({"f": nome, "w": w}))
        assert b[:3] == b"\xff\xd8\xff" and len(b) > 20000, (chave, len(b))
        open(out, "wb").write(b); time.sleep(3)
    m = meta.get("File:" + nome.replace("_", " "), {})
    lista[chave] = dict(arquivo=f"commons/{chave}.jpg", descricao=desc, commons="File:" + nome,
                        pagina="https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(nome.replace(" ", "_")), **m)
    print(chave, os.path.getsize(out), m.get("licenca"), "|", m.get("autor"))
json.dump(lista, open("imagens/lista_commons.json", "w"), ensure_ascii=False, indent=1)
