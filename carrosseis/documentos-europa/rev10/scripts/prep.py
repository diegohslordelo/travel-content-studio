"""Prepara os insumos do carrossel (rode de dentro de rev1/): python3 scripts/prep.py

1. tokens.css: variáveis CSS lidas direto de design-system/primeiro-dia-tokens-v2.json
   (nenhum valor visual é digitado à mão no slides.html).
A foto da capa vem de foto enviada pelo Diego, não de fotograma de vídeo.
"""
import json
from pathlib import Path

TOKENS = Path("../../../design-system/primeiro-dia-tokens-v2.json")


def folhas(d, caminho=""):
    for k, v in d.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict) and "$value" not in v:
            yield from folhas(v, f"{caminho}{k}.")
        elif isinstance(v, dict):
            yield caminho + k, v["$value"]


def valor(v):
    if isinstance(v, dict) and "hex" in v:
        return v["hex"]
    if isinstance(v, dict) and "value" in v and "unit" in v:
        return f"{v['value']}{v['unit']}"
    return str(v)


def tokens_css():
    t = {k: valor(v) for k, v in folhas(json.loads(TOKENS.read_text()))}
    pegar = {
        "--pd-y": "color.signal.500", "--pd-y7": "color.signal.700",
        "--pd-n": "color.night.900", "--pd-n5": "color.night.500", "--pd-n3": "color.night.300",
        "--pd-p": "color.paper.500", "--pd-r": "color.paper.0", "--pd-ink": "color.ink.500", "--pd-g": "color.exit.600",
        "--pd-radius-paper": "radius.paper", "--pd-radius-tag": "radius.tag",
        "--pd-radius-plate": "radius.plate", "--pd-radius-photo": "radius.photo",
        "--pd-sh-plate": "shadow.shadow-plate", "--pd-bevel": "shadow.shadow-plate-bevel",
        "--pd-sh-paper": "shadow.shadow-paper",
        "--pd-grain-op": "opacity.op-grain", "--pd-fiber-op": "opacity.op-fiber", "--pd-scrim-op": "opacity.op-scrim",
        "--pd-w": "layout.carousel.width", "--pd-h": "layout.carousel.height", "--pd-m": "layout.carousel.margin",
    }
    linhas = [f"  {css}: {t[chave]};" for css, chave in pegar.items()]
    Path("tokens.css").write_text(
        "/* Gerado por scripts/prep.py a partir de design-system/primeiro-dia-tokens-v2.json. Não editar à mão. */\n"
        ":root{\n" + "\n".join(linhas) + "\n}\n"
    )



if __name__ == "__main__":
    tokens_css()
    print("ok: tokens.css")
