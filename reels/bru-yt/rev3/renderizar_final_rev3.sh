#!/usr/bin/env bash
# Render final da REV3 em 1920 × 1080, 30 fps (de reels/bru-yt). Receita de Amsterdam (docs/VIDEO_LONGO_PASSO_A_PASSO.md,
# seção 7): 16 partes do proxy 1080p (x264 fast, CRF 19, teto de 12 Mbps), cada uma refeita só se faltar (o container
# pode reiniciar); imagem juntada sem recodificar; o som de cada parte (só efeitos do Remotion) cortado no tamanho
# exato da imagem; mixagem da REV3 (voz, narrações, música, efeitos, −14 LUFS, limitador −2 dBTP) e correção de pico
# pós-AAC (corrigir_pico_aac.py, AAC 192 kbps 48 kHz); medição no arquivo exportado (padrão de áudio, 11.3).
# Precisa do proxy servido:  node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
set -euo pipefail
cd "$(dirname "$0")/.."
FPS=30
RM=../../design-system/remotion
D=_tmp/final_rev3
mkdir -p "$D"
TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/props_rev3.json'))['duracao'] * $FPS / 1000))")
PARTES=16
: > "$D/v.txt"; : > "$D/a.txt"
for i in $(seq 0 $((PARTES - 1))); do
  q0=$(( TOTAL * i / PARTES )); q1=$(( TOTAL * (i + 1) / PARTES - 1 ))
  f="$D/h_$i.mp4"
  if [ ! -s "$f" ]; then
    echo "== parte $((i + 1))/$PARTES: quadros $q0–$q1 ($(date +%H:%M))"
    rm -rf _tmp/rtmp && mkdir -p _tmp/rtmp
    (cd "$RM" && TMPDIR="$OLDPWD/_tmp/rtmp" X264_PRESET=fast CRF=19 MAXRATE=12M node scripts/videolongo.mjs ../../reels/bru-yt/rev3/props_rev3.json ../../reels/bru-yt/public trecho "../../reels/bru-yt/$f.tmp.mp4" "$q0" "$q1" 1) 2>&1 | grep -E "^ok|rror" | tail -1
    mv "$f.tmp.mp4" "$f"
  fi
  n=$(( q1 - q0 + 1 ))
  ffmpeg -nostdin -v error -y -i "$f" -map 0:v -c copy "$f.v.mp4"
  ffmpeg -nostdin -v error -y -i "$f" -map 0:a -af "apad,atrim=end=$(python3 -c "print($n / $FPS)")" -ar 48000 -ac 2 -c:a pcm_f32le "$f.a.wav"
  echo "file '$(basename "$f").v.mp4'" >> "$D/v.txt"
  echo "file '$(basename "$f").a.wav'" >> "$D/a.txt"
done
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$D/v.txt" -c copy -movflags +faststart "$D/video.mp4"
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$D/a.txt" -c:a pcm_f32le "$D/sfx.wav"
rm -f "$D"/h_*.mp4.v.mp4 "$D"/h_*.mp4.a.wav
python3 -I rev3/mixar_rev3.py --saida "$D/mix.wav" --sfx "$D/sfx.wav" | tail -1
python3 -I rev3/corrigir_pico_aac.py "$D/mix.wav" "$D/video.mp4" _tmp/rev3_final_1080p.mp4 192k
ffmpeg -nostdin -hide_banner -i _tmp/rev3_final_1080p.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A15 Summary | grep -E "I:|Peak:"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration,bit_rate -of compact _tmp/rev3_final_1080p.mp4
echo "FIM $(date +%H:%M)"
