#!/usr/bin/env bash
# Extrai os 6 quadros do carrossel dos brutos em ../fonte/ (fora do git).
# Rodar de dentro de carrosseis/bruges-dicas/rev1/. Requer ffmpeg e Python com Pillow.
# Cada linha: arquivo, segundo, rotação (0 = nenhuma; cw = 90° horário), recorte (L:A:X:Y no quadro 3840x2160 já orientado), saída.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p _tmp fotos
extrai() { # arquivo seg rot saida
  ffmpeg -v error -y -ss "$2" -i "../fonte/$1.MOV" -frames:v 1 "_tmp/$4.png"
  python3 -I - "$4" "$3" <<'PY'
import sys
from PIL import Image
n, rot = sys.argv[1], sys.argv[2]
im = Image.open(f'_tmp/{n}.png')
if rot == 'cw': im = im.transpose(Image.ROTATE_270)
im.save(f'_tmp/{n}_or.png')
print(n, im.size)
PY
}
extrai IMG_2549 3    0  capa
extrai IMG_2624 8.18 0  fritbar
extrai IMG_2700 4    0  chez
extrai IMG_2650 1    0  minnewater
extrai IMG_2696 16   cw cerveja
