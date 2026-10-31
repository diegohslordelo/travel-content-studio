"""Baixa as fotos do Wikimedia Commons usadas no Reel (thumb.php, com pausa e nova tentativa no 429) e guarda a licença.
Uso (de dentro de reels/darvaza-cratera/): python3 scripts/baixar_imagens.py"""
import json, os, time, urllib.parse, urllib.request, urllib.error
UA = {"User-Agent": "PrimeiroDiaReel/1.0 (diegohs.lordelo@gmail.com)"}
FOTOS = {
    "chamas_perto": ("DarvazaMay2011.JPG", 3000),
    "brilho_anoitecer": ("Glow of Darvaza gas crater, Jähennem derwezesi, Door to Hell, Gates of Hell, Derweze, Turkmenistan.jpg", 3000),
    "borda_noite": ("Darvaza Gas Crater (42435082502).jpg", 3000),
    "cratera_dia": ("Darvaza Gas Crater - Daytime (42435086112).jpg", 3000),
    "dentro_fogo": ("Inside Darvaza gas crater, Jähennem derwezesi, Door to Hell, Gates of Hell, Derweze, Turkmenistan.jpg", 3000),
    "bracos_abertos": ("Darvasa gas crater 2.jpg", 3000),
    "carro_borda": ("Derweze gas fire2.jpg", 3000),
    "noite_deserto": ("Darvaza gas crater, Jähennem derwezesi, Door to Hell, Gates of Hell, Derweze, Turkmenistan at night.jpg", 3000),
    "amanhecer_longe": ("Darvaza gas crater, Jähennem derwezesi, Door to Hell, Gates of Hell, Derweze, Turkmenistan at dawn.jpg", 3000),
    "porta_inferno": ("The Door to Hell.jpg", 3000),
    "brilho_crepusculo": ("Gates of Hell 015 (8031716278).jpg", 2816),
    "estrelas": ("Star trails over Turkmenistan sky.jpg", 3000),
    "fogo_dia": ("Darvaza gas crater, Jähennem derwezesi, Door to Hell, Gates of Hell, Derweze, Turkmenistan.jpg", 3000),
    "vermelho_dentro": ("Darvaza Gas Crater (42435087502).jpg", 1920),
    "panorama": ("Darvasa gas crater panorama crop.jpg", 5934),
    "silhuetas_borda": ("Darvasa gas crater 1.jpg", 3000),
    "fumaca_noite": ("Darvaza Gas Crater (42435084232).jpg", 3000),
}
meta_all = {}
for f in ["/tmp/commons_darvaza2.json"]:
    if os.path.exists(f): meta_all.update(json.load(open(f)))
def get(u):
    for k in range(10):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(int(e.headers.get("retry-after", "30")) + 3)
    raise SystemExit("429 persistente")
lista = {}
for chave, (nome, w) in FOTOS.items():
    out = f"imagens/commons/{chave}.jpg"
    if not (os.path.exists(out) and os.path.getsize(out) > 20000):
        d = get("https://commons.wikimedia.org/w/thumb.php?" + urllib.parse.urlencode({"f": nome, "w": w}))
        assert d[:3] == b"\xff\xd8\xff" and len(d) > 20000, (chave, len(d))
        open(out, "wb").write(d); time.sleep(3)
    m = meta_all.get("File:" + nome, {})
    lista[chave] = {"arquivo": f"commons/{chave}.jpg", "commons": "File:" + nome, "pagina": "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(nome.replace(" ", "_")),
                    "autor": m.get("artist"), "licenca": m.get("lic"), "data": m.get("date")}
    print(chave, os.path.getsize(out), m.get("lic"), m.get("artist"))
json.dump(lista, open("imagens/lista_commons.json", "w"), ensure_ascii=False, indent=1)
