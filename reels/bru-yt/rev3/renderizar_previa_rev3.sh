#!/usr/bin/env bash
# Prévia completa da REV3 (960 × 540, 30 fps), de reels/bru-yt. Precisa do proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# 4 partes (cada uma só é refeita se faltar) → imagem juntada sem recodificar → efeitos sonoros do Remotion somados à
# mixagem da REV3 (rev3/mixar_rev3.py, −14 LUFS) → rev3/previas/rev3_previa_540p.mp4 (H.264 CRF 27 + AAC 160 kbps).
set -euo pipefail
cd "$(dirname "$0")/.."
FPS=30
RM=../../design-system/remotion
TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/props_rev3.json'))['duracao'] * $FPS / 1000))")
mkdir -p _tmp/previa_rev3 rev3/previas
: > _tmp/previa_rev3/v.txt; : > _tmp/previa_rev3/a.txt
PARTES=4
for i in $(seq 0 $((PARTES - 1))); do
  q0=$(( TOTAL * i / PARTES )); q1=$(( TOTAL * (i + 1) / PARTES - 1 ))
  f="_tmp/previa_rev3/parte$i.mp4"
  if [ ! -s "$f" ]; then
    echo "== parte $i: quadros $q0–$q1"
    rm -rf _tmp/rtmp && mkdir -p _tmp/rtmp
    (cd "$RM" && TMPDIR="$OLDPWD/_tmp/rtmp" CRF=26 X264_PRESET=veryfast node scripts/videolongo.mjs ../../reels/bru-yt/rev3/props_rev3.json ../../reels/bru-yt/public trecho "../../reels/bru-yt/$f.tmp.mp4" "$q0" "$q1" 0.5) 2>&1 | grep -v -i "memory\|docker" | tail -1
    mv "$f.tmp.mp4" "$f"
  fi
  n=$(( q1 - q0 + 1 ))
  ffmpeg -nostdin -v error -y -i "$f" -map 0:v -c copy "$f.v.mp4"
  ffmpeg -nostdin -v error -y -i "$f" -map 0:a -af "apad,atrim=end=$(python3 -c "print($n / $FPS)")" -ar 48000 -ac 2 -c:a pcm_f32le "$f.a.wav"
  echo "file '$(basename "$f").v.mp4'" >> _tmp/previa_rev3/v.txt
  echo "file '$(basename "$f").a.wav'" >> _tmp/previa_rev3/a.txt
done
ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/previa_rev3/v.txt -c copy _tmp/previa_rev3/video.mp4
ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/previa_rev3/a.txt -c:a pcm_f32le _tmp/previa_rev3/sfx.wav
python3 -I rev3/mixar_rev3.py --saida _tmp/previa_rev3/mix.wav --sfx _tmp/previa_rev3/sfx.wav | tail -1
ffmpeg -nostdin -v error -y -i _tmp/previa_rev3/video.mp4 -i _tmp/previa_rev3/mix.wav -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 160k -shortest -movflags +faststart rev3/previas/rev3_previa_540p.mp4
ls -la rev3/previas/rev3_previa_540p.mp4
