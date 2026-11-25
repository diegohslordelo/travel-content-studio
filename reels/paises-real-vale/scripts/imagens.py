# Baixa as imagens de apoio do Wikimedia Commons (licença livre), com metadados de licença.
# Uso (de dentro da pasta do Reel): python3 scripts/imagens.py rev1
# Lê rev1/imagens.json: {"nome": "File:...", ...} ou {"nome": {"busca": "termos"}} e grava em _tmp/public/img/ + rev1/licencas.json
import json, os, sys, time, urllib.parse, urllib.request
rev = sys.argv[1]
UA = {"User-Agent": "MediaResearchScript/1.0 (non-commercial short video; python-urllib)"}
cfg = json.load(open(f"{rev}/imagens.json"))
os.makedirs("_tmp/public/img", exist_ok=True)
lic_path = f"{rev}/licencas.json"
lic = json.load(open(lic_path)) if os.path.exists(lic_path) else {}

def get(url, tent=12):
    for k in range(tent):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except Exception as e:
            espera = min(300, 15 * (k + 1))
            print(f"  erro {e} · esperando {espera}s", flush=True)
            time.sleep(espera)
    raise SystemExit(f"falhou: {url}")

def api(params):
    return json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"format": "json", **params})))

for nome, alvo in cfg.items():
    if nome.startswith("_"):
        continue
    dest = f"_tmp/public/img/{nome}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 1000 and nome in lic:
        continue
    if isinstance(alvo, dict):
        r = api({"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {alvo['busca']}", "gsrnamespace": 6, "gsrlimit": 10,
                 "prop": "imageinfo", "iiprop": "url|size|extmetadata"})
        pags = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0))
        print(f"== {nome}: busca '{alvo['busca']}'")
        for p in pags:
            ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
            print("   ", p["title"], ii["width"], "x", ii["height"], "|", m.get("LicenseShortName", {}).get("value", ""))
        time.sleep(6)
        continue
    r = api({"action": "query", "titles": alvo, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1600})
    p = list(r["query"]["pages"].values())[0]
    ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
    dados = get(ii["thumburl"])
    if len(dados) < 1000 or dados[:2] != b"\xff\xd8":
        print(f"  {nome}: download inválido"); time.sleep(10); continue
    open(dest, "wb").write(dados)
    import re
    limpa = lambda s: re.sub("<[^>]+>", "", s or "").strip()
    lic[nome] = {"arquivo": alvo, "pagina": ii.get("descriptionurl"), "licenca": m.get("LicenseShortName", {}).get("value"),
                 "autor": limpa(m.get("Artist", {}).get("value")), "credito": limpa(m.get("Credit", {}).get("value"))[:200]}
    json.dump(lic, open(lic_path, "w"), ensure_ascii=False, indent=1)
    print(f"ok {nome} ← {alvo} ({lic[nome]['licenca']})", flush=True)
    time.sleep(5)
