#!/usr/bin/env bash
# Reel "Basílica do Sangue Sagrado" · REV2: preparar → render (Remotion) → master → capa.
# Roda de dentro de reels/bruges-sangue/rev2:  bash scripts/render.sh   (PY = python com numpy, soundfile, scipy)
set -euo pipefail
PY=${PY:-python3}
AQUI=$(pwd)
PUB="$AQUI/_tmp/public"
RM="$AQUI/../../../design-system/remotion"

$PY scripts/preparar.py

# render: H.264 em qualidade máxima prática (CRF 10, preset slow); o Instagram recomprime na subida
( cd "$RM" && npx remotion render Bruges "$AQUI/_tmp/render.mkv" --props="$PUB/props.json" --public-dir="$PUB" \
    --codec=h264 --crf=10 --x264-preset=slow --pixel-format=yuv420p --audio-codec=pcm-16 --concurrency=4 --log=error )

# master: ganho linear + limitador (4× sobreamostragem) até −14 LUFS integrados e pico verdadeiro ≤ −1 dBTP (DS V2, 4.6)
ffmpeg -v error -y -i _tmp/render.mkv -vn -ac 2 -ar 48000 -c:a pcm_f32le _tmp/mix.wav
I=$(ffmpeg -hide_banner -nostats -i _tmp/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+I:' | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14.0 - ($I) + 0.2, 2))")  # +0,2 dB compensa o que o limitador tira
ffmpeg -v error -y -i _tmp/mix.wav -af "volume=${G}dB,aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=false,aresample=48000" -c:a pcm_f32le _tmp/master.wav
ffmpeg -v error -y -i _tmp/render.mkv -i _tmp/master.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -movflags +faststart \
  reel_bruges-sangue_rev2.mp4

# capa: quadro com o gancho completo e o frasco ("DE JESUS CRISTO?")
ffmpeg -v error -y -ss 6.35 -i reel_bruges-sangue_rev2.mp4 -frames:v 1 -q:v 2 capa_bruges-sangue_rev2.jpg
echo "ok: reel_bruges-sangue_rev2.mp4"
