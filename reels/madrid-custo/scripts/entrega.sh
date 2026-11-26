#!/bin/sh
# Vídeo de entrega para o GitHub (arquivo comum, sem LFS: a cota do repositório está esgotada).
# Recodifica o master (−14 LUFS, já pronto) em H.264 2 passadas a 12 Mbps → ~85 MB para ~56 s, abaixo do limite de 100 MB.
# O áudio é copiado sem mexer (o loudness do master fica igual). Uso (de dentro de reels/madrid-custo/): REV=rev2 sh scripts/entrega.sh
set -e
REV=${REV:-rev2}
M=$REV/reel_madrid-custo_$REV.mp4
# o master fica em _tmp/ (se o script parar no meio, roda de novo a partir dele)
[ -f _tmp/master_$REV.mp4 ] || mv "$M" _tmp/master_$REV.mp4
ffmpeg -v error -y -i _tmp/master_$REV.mp4 -c:v libx264 -preset slow -b:v 12M -maxrate 16M -bufsize 24M -pass 1 -passlogfile _tmp/x264 -an -f mp4 /dev/null
ffmpeg -v error -y -i _tmp/master_$REV.mp4 -c:v libx264 -preset slow -b:v 12M -maxrate 16M -bufsize 24M -pass 2 -passlogfile _tmp/x264 -pix_fmt yuv420p -c:a copy -movflags +faststart "$M"
ls -la "$M"
