"""Recorta os quadros extraídos (extrair_fotos_rev1.sh) para os slides. Roda de dentro de rev1/.
Sem filtro nem correção de cor ("Real antes de bonito", DS V2 1.1)."""
from PIL import Image
# nome: (x0, y0, largura, altura) no quadro 3840x2160 orientado; saída em px do slide x2 para nitidez
RECORTES = {
    'capa':       ((1500, 0, 1620, 2160), (1080, 1440)),   # 3:4 sangria
    'fritbar':    ((300, 0, 2880, 2160), (1380, 1035)),    # 4:3
    'chez':       ((300, 0, 2880, 2160), (1380, 1035)),
    'minnewater': ((300, 0, 2880, 2160), (1380, 1035)),
    'cerveja':    ((700, 0, 2880, 2160), (1380, 1035)),
}
for nome, ((x, y, w, h), saida) in RECORTES.items():
    im = Image.open(f'_tmp/{nome}_or.png').convert('RGB').crop((x, y, x + w, y + h)).resize(saida, Image.LANCZOS)
    im.save(f'fotos/{nome}.jpg', quality=90)
    print(nome, im.size)
