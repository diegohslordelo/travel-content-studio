#!/usr/bin/env bash
# Render final da REV3 em 3840 × 2160, 30 fps (de reels/bru-yt). Pedido do Diego (07/11/2026): o final é em 4K.
# Receita do 4K de Amsterdam (reels/ams-yt/rev3/renderizar_rev3.sh, modo final4k), adaptada para 30 fps:
#   - imagem lida direto da fonte 4K (HEVC 10 bits; o Chromium não decodifica HEVC e o Remotion cai no <OffthreadVideo>);
#   - 16 partes em escala 2, x264 fast, CRF 19, teto de 20 Mbps (o YouTube recodifica tudo), cada uma refeita só se
#     faltar (o container pode reiniciar) e gravada só quando termina (parte pela metade nunca passa por pronta);
#   - CONCURRENCY=3 e OFFTHREAD_CACHE_MB=1500 seguram a memória (com os padrões, a máquina de 15 GB reiniciou no 4K);
#   - imagem juntada sem recodificar e sem copiar as partes (lista do concat com a duração exata de cada parte), o som
#     de cada parte (só efeitos do Remotion) cortado no tamanho exato da imagem; as partes só saem depois de conferir
#     que o vídeo juntado tem todos os quadros;
#   - mixagem da REV3 (mixar_rev3.py) e correção de pico pós-AAC (corrigir_pico_aac.py, AAC 192 kbps 48 kHz);
#   - medição no arquivo exportado (padrão de áudio, 11.3).
# Precisa da fonte servida:  node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
set -euo pipefail
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
FPS=30
RM=../../design-system/remotion
D=_tmp/final4k_rev3
SAIDA=_tmp/rev3_final_4k.mp4
mkdir -p "$D" _tmp/servir
export BUNDLE_DIR="$RAIZ/_tmp/bundle4k"
[ -n "${MANTER_BUNDLE:-}" ] || rm -rf "$BUNDLE_DIR"  # bundle velho renderiza o código velho do Remotion
ln -sf "$RAIZ/fonte/1103_fala.mp4" _tmp/servir/fonte4k.mp4
python3 -c "
import json; p = json.load(open('rev3/props_rev3.json')); p['video'] = 'http://127.0.0.1:8787/fonte4k.mp4'
json.dump(p, open('_tmp/props_rev3_4k.json', 'w'), ensure_ascii=False)"
TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/props_rev3.json'))['duracao'] * $FPS / 1000))")
PARTES=16
: > "$D/v.txt"; : > "$D/a.txt"
soma=0
for i in $(seq 0 $((PARTES - 1))); do
  q0=$(( TOTAL * i / PARTES )); q1=$(( TOTAL * (i + 1) / PARTES - 1 ))
  f="$D/f_$i.mp4"
  if [ ! -s "$f" ]; then
    echo "== parte $((i + 1))/$PARTES: quadros $q0–$q1 ($(date +%H:%M))"
    rm -rf /tmp/remotion-v*-assets* _tmp/rtmp 2>/dev/null || true; mkdir -p _tmp/rtmp
    if ! (cd "$RM" && TMPDIR="$RAIZ/_tmp/rtmp" CONCURRENCY=3 OFFTHREAD_CACHE_MB=1500 X264_PRESET=fast CRF=19 MAXRATE=20M \
          node scripts/videolongo.mjs "$RAIZ/_tmp/props_rev3_4k.json" "$RAIZ/public" trecho "$RAIZ/$f.tmp.mp4" "$q0" "$q1" 2) > "$D/parte_$i.log" 2>&1; then
      grep -v "%$" "$D/parte_$i.log" | tail -20; exit 1
    fi
    mv "$f.tmp.mp4" "$f"
    echo "   ok ($(date +%H:%M))"
  fi
  n=$(( q1 - q0 + 1 ))
  q=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$f")
  [ "$q" -eq "$n" ] || { echo "parte $i: $q quadros, esperado $n"; exit 1; }
  soma=$(( soma + n ))
  ffmpeg -nostdin -v error -y -i "$f" -map 0:a -af "apad,atrim=end=$(python3 -c "print($n / $FPS)")" -ar 48000 -ac 2 -c:a pcm_f32le "$f.a.wav"
  printf "file '%s'\nduration %s\n" "$(basename "$f")" "$(python3 -c "print($n / $FPS)")" >> "$D/v.txt"
  echo "file '$(basename "$f").a.wav'" >> "$D/a.txt"
done
rm -rf /tmp/remotion-v*-assets* _tmp/rtmp 2>/dev/null || true  # a cópia da fonte 4K não serve mais
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$D/v.txt" -map 0:v -c copy -movflags +faststart "$D/video.mp4"
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$D/a.txt" -c:a pcm_f32le "$D/sfx.wav"
qv=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$D/video.mp4")
[ "$qv" -eq "$TOTAL" ] && [ "$soma" -eq "$TOTAL" ] || { echo "vídeo juntado: $qv quadros, esperado $TOTAL"; exit 1; }
python3 -I rev3/mixar_rev3.py --saida "$D/mix.wav" --sfx "$D/sfx.wav" | tail -1
python3 -I rev3/corrigir_pico_aac.py "$D/mix.wav" "$D/video.mp4" "$SAIDA" 192k
rm -f "$D/video.mp4" "$D"/f_*.mp4 "$D"/f_*.mp4.a.wav  # partes só saem com o arquivo final pronto
ffmpeg -nostdin -hide_banner -i "$SAIDA" -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A15 Summary | grep -E "I:|Peak:"
ffprobe -v error -show_entries stream=codec_type,codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,duration,bit_rate -of compact "$SAIDA"
echo "FIM $(date +%H:%M)"
