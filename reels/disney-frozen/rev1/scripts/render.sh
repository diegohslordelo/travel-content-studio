#!/usr/bin/env bash
# Reel do Frozen · REV1: preparar → render (Remotion, composição "Frozen") → master → capa.
# Roda de dentro de reels/disney-frozen/rev1:  bash scripts/render.sh
# Antes (uma vez): python3 scripts/recorte.py (recorte por IA) e python3 scripts/alinhar.py (tempo de cada palavra).
# Os prints entram sozinhos quando estiverem em imagens/ (comentario_borrado.png, site_oficial.png, frozen_show.jpg);
# enquanto faltar algum, sai o cartão provisório listrado e o arquivo ganha o sufixo _provisorio.
set -euo pipefail
PY=${PY:-python3}
AQUI=$(pwd)
PUB="$AQUI/_tmp/public"
RM="$AQUI/../../../design-system/remotion"

$PY scripts/preparar.py
SUF=$($PY -c "import json; print('_provisorio' if json.load(open('_tmp/montagem.json'))['provisorios'] else '')")

( cd "$RM" && npx remotion render Frozen "$AQUI/_tmp/render.mkv" --props="$PUB/props.json" --public-dir="$PUB" \
    --codec=h264 --crf=10 --x264-preset=slow --pixel-format=yuv420p --audio-codec=pcm-16 --concurrency=4 --log=error )

# master: ganho linear + limitador (4× sobreamostragem) até −14 LUFS integrados e pico verdadeiro ≤ −1 dBTP (DS V2, 4.6)
ffmpeg -v error -y -i _tmp/render.mkv -vn -ac 2 -ar 48000 -c:a pcm_f32le _tmp/mix.wav
I=$(ffmpeg -hide_banner -nostats -i _tmp/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+I:' | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14.0 - ($I), 2))")
ffmpeg -v error -y -i _tmp/mix.wav -af "volume=${G}dB,aresample=192000,alimiter=limit=0.84:attack=1:release=60:level=false,aresample=48000" -c:a pcm_f32le _tmp/master.wav
ffmpeg -v error -y -i _tmp/render.mkv -i _tmp/master.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 320k -ar 48000 -movflags +faststart \
  "reel_disney-frozen_rev1${SUF}.mp4"
# versão de postar (CRF 18, ≈ 2 MB/s): o Instagram recomprime na subida
ffmpeg -v error -y -i "reel_disney-frozen_rev1${SUF}.mp4" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart "reel_disney-frozen_rev1${SUF}_postar.mp4"

# capa: quadro com o gancho completo ("PRO PARQUE." na tela) e a fita sobre o castelo
ffmpeg -v error -y -ss 2.9 -i "reel_disney-frozen_rev1${SUF}.mp4" -frames:v 1 -q:v 2 "capa_disney-frozen_rev1${SUF}.jpg"
echo "ok: reel_disney-frozen_rev1${SUF}.mp4"
