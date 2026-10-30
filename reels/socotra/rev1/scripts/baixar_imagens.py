"""Baixa as fotos de Socotra do Wikimedia Commons (thumb.php, pausa de 3 s) e guarda licença, autor e fonte.

Uso (de dentro de reels/socotra/rev1/): python3 scripts/baixar_imagens.py
Gera imagens/web/<id>.jpg e imagens/meta_commons.json. Só arquivos com licença livre (CC BY, CC BY-SA, domínio público).
"""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "PrimeiroDiaReel/1.0 (https://instagram.com/primeirodiaem)"
FOTOS = {
    "firmihin_aurora": ("Centennial Dragon blood trees at dawn on Firmhin Plateau, Socotra, Yemen (16678684240).jpg", 3000),
    "dragoes_ilha": ("Dragon blood trees in Socotra Island, Yemen.jpg", 3000),
    "dragao_2": ("Dragonblood tree in Socotra 2.jpg", 1800),
    "diksam": ("Dragon’s blood trees, Diksam plateau, Socotra Island.jpg", 1600),
    "resina_seca": ("Dried Dragons Blood, Socotra Island (10099129506).jpg", 1800),
    "garrafas": ("Bottle Trees, Socotra Is (12448230015).jpg", 3000),
    "rosa_deserto": ("Desert Rose, Socotra Is (17131661372).jpg", 1800),
    "dunas_noget": ("Noget Sand Dunes, Socotra, Yemen.jpg", 3000),
    "skand": ("Socotra Mt. Skand.jpg", 1800),
    "dragao_guarda": ("Dracaena cinnabari (34924435216).jpg", 3202),
    "iss_costa": ("The southern coast of Yemeni's island of Socotra (iss069e004768).jpg", 3000),
}


def get(url, tentativas=6):
    """GET com espera crescente quando o Commons responde 429 (limite de pedidos)."""
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tentativas - 1:
                raise
            time.sleep(20 * (k + 1))


def main():
    os.makedirs("imagens/web", exist_ok=True)
    titulos = "|".join("File:" + t for t, _ in FOTOS.values())
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "titles": titulos, "prop": "imageinfo", "iiprop": "extmetadata|url|size", "format": "json",
        "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|ImageDescription|DateTimeOriginal"})
    d = json.loads(get(api))
    norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
    info = {}
    for p in d["query"]["pages"].values():
        ii = p["imageinfo"][0]
        m = {k: re.sub("<[^>]+>", "", v["value"]).strip() for k, v in ii["extmetadata"].items()}
        info[p["title"]] = {"licenca": m.get("LicenseShortName"), "licenca_url": m.get("LicenseUrl"), "autor": m.get("Artist"),
                            "descricao": m.get("ImageDescription", "")[:300], "data": m.get("DateTimeOriginal"),
                            "pagina": ii["descriptionurl"], "tamanho": [ii["width"], ii["height"]]}
    meta = {}
    for k, (t, w) in FOTOS.items():
        dest = f"imagens/web/{k}.jpg"
        tit = "File:" + t
        meta[k] = {"arquivo": dest, "titulo": t, **info.get(tit, info.get(norm.get(tit, ""), {}))}
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            continue
        for tentativa in range(4):
            try:
                b = get("https://commons.wikimedia.org/w/thumb.php?" + urllib.parse.urlencode({"f": t, "w": w}))
                if b[:2] == b"\xff\xd8" and len(b) > 1000:
                    open(dest, "wb").write(b)
                    print("ok", k, len(b) // 1024, "kB")
                    break
                print("inválido", k, b[:60])
            except Exception as e:
                print("erro", k, e)
            time.sleep(10 * (tentativa + 1))
        time.sleep(3)
    json.dump(meta, open("imagens/meta_commons.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
