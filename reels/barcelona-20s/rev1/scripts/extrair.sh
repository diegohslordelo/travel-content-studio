#!/usr/bin/env bash
# Extrai proxies de análise (1280 px no lado maior, 12 fps), WAV mono 16 kHz e folhas 1 fps.
# Roda de dentro de reels/barcelona-20s. Não altera o material bruto.
set -euo pipefail
SRC=../../material/extras
for f in "$SRC"/*; do
  b=$(basename "${f%.*}")
  [ -f _tmp/proxy/$b.mp4 ] || ffmpeg -v error -y -i "$f" -map 0:v:0 -vf "scale='if(gt(iw,ih),1280,-2)':'if(gt(iw,ih),-2,1280)',fps=12" -c:v libx264 -crf 20 -preset veryfast _tmp/proxy/$b.mp4
  [ -f _tmp/wav/$b.wav ] || ffmpeg -v error -y -i "$f" -map 0:a:0 -ac 1 -ar 16000 _tmp/wav/$b.wav
  [ -f _tmp/folhas/$b.jpg ] || ffmpeg -v error -y -i "$f" -map 0:v:0 -vf "fps=2,scale='if(gt(iw,ih),320,-2)':'if(gt(iw,ih),-2,320)',drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x12:padding=2" -frames:v 1 _tmp/folhas/$b.jpg
  echo "$b ok"
done
