#!/bin/bash
# Render da REV1 do Reel BXL-decepção. Roda de reels/bxl-decepcao, depois de:
#   python3 rev1/decupar_voz.py && python3 rev1/montar_rev1.py && python3 -I rev1/mixar_rev1.py
#
#   bash rev1/renderizar_rev1.sh quadros N1 N2 …   quadros soltos (PNG) em _tmp/quadros/ para conferir
#   bash rev1/renderizar_rev1.sh final               vídeo inteiro: imagem do Remotion + som da mixagem
#
# Saída do "final" (rev1/):
#   reel_bxl-decepcao_rev1.mp4              1080×1920, 24 qps, H.264 CRF 17, AAC 320 kb/s (com a trilha)
#   reel_bxl-decepcao_rev1_sem_trilha.mp4   voz + efeitos (para usar música da biblioteca do Instagram, baixa)
#   reel_bxl-decepcao_rev1_previa.mp4       prévia leve (720p, ~2 Mb/s)
set -euo pipefail
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
REM=../../design-system/remotion
PROPS="$RAIZ/rev1/props_rev1.json"
PUB="$RAIZ/public"
mkdir -p _tmp/quadros

case "${1:-}" in
  quadros)
    shift
    for n in "$@"; do
      (cd "$REM" && npx remotion still ReelFormato "$RAIZ/_tmp/quadros/q$(printf %04d "$n").png" --frame="$n" --props="$PROPS" --public-dir="$PUB" --log=error)
      echo "ok _tmp/quadros/q$(printf %04d "$n").png"
    done
    ;;
  final)
    rm -rf /tmp/remotion-v*-assets* 2>/dev/null || true
    (cd "$REM" && npx remotion render ReelFormato "$RAIZ/_tmp/video_mudo.mp4" --props="$PROPS" --public-dir="$PUB" \
       --codec=h264 --crf=17 --pixel-format=yuv420p --color-space=bt709 --muted --concurrency=4 --log=error)
    for v in "" "_sem_trilha"; do
      if [ -z "$v" ]; then som=_tmp/mix_master.wav; else som=_tmp/mix_sem_trilha.wav; fi
      ffmpeg -v error -y -i _tmp/video_mudo.mp4 -i "$som" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 \
        -shortest -movflags +faststart "rev1/reel_bxl-decepcao_rev1${v}.mp4"
      echo "ok rev1/reel_bxl-decepcao_rev1${v}.mp4"
    done
    ffmpeg -v error -y -i rev1/reel_bxl-decepcao_rev1.mp4 -vf scale=720:-2 -c:v libx264 -preset slow -b:v 2M -maxrate 2.5M -bufsize 4M \
      -c:a aac -b:a 128k -movflags +faststart rev1/reel_bxl-decepcao_rev1_previa.mp4
    echo "ok rev1/reel_bxl-decepcao_rev1_previa.mp4"
    ;;
  *)
    echo "uso: bash rev1/renderizar_rev1.sh quadros N… | final"; exit 1 ;;
esac
