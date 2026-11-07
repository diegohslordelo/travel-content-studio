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
#   - timestamps da imagem conferidos e corrigidos (corrigir_ts_video.py);
#   - medição no arquivo exportado (padrão de áudio, 11.3).
# Se o container reiniciar no meio das partes: SUBPARTES=4 MANTER_BUNDLE=1 bash rev3/renderizar_final4k_rev3.sh
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
    # SUBPARTES > 1 (07/11/2026: o container reiniciou 3 vezes no meio de uma parte): cada parte sai em pedaços
    # menores, cada um guardado ao terminar; os pedaços são juntados na parte (imagem sem recodificar, som cortado
    # no tamanho exato de cada pedaço)
    S=${SUBPARTES:-1}
    : > "$D/sub_v.txt"; : > "$D/sub_a.txt"
    for k in $(seq 0 $((S - 1))); do
      s0=$(( q0 + (q1 - q0 + 1) * k / S )); s1=$(( q0 + (q1 - q0 + 1) * (k + 1) / S - 1 ))
      g="$f.s$k.mp4"; [ "$S" -eq 1 ] && g="$f.tmp.mp4"
      if [ ! -s "$g" ] || [ "$S" -eq 1 ]; then
        rm -rf /tmp/remotion-v*-assets* _tmp/rtmp 2>/dev/null || true; mkdir -p _tmp/rtmp
        if ! (cd "$RM" && TMPDIR="$RAIZ/_tmp/rtmp" CONCURRENCY=3 OFFTHREAD_CACHE_MB=1500 X264_PRESET=fast CRF=19 MAXRATE=20M \
              node scripts/videolongo.mjs "$RAIZ/_tmp/props_rev3_4k.json" "$RAIZ/public" trecho "$RAIZ/$g.tmp.mp4" "$s0" "$s1" 2) > "$D/parte_${i}_$k.log" 2>&1; then
          grep -v "%$" "$D/parte_${i}_$k.log" | tail -20; exit 1
        fi
        mv "$g.tmp.mp4" "$g"
        [ "$S" -gt 1 ] && echo "   pedaço $((k + 1))/$S ok ($(date +%H:%M))"
      fi
      m=$(( s1 - s0 + 1 ))
      printf "file '%s'\nduration %s\n" "$(basename "$g")" "$(python3 -c "print($m / $FPS)")" >> "$D/sub_v.txt"
      ffmpeg -nostdin -v error -y -i "$g" -map 0:a -af "apad,atrim=end=$(python3 -c "print($m / $FPS)")" -ar 48000 -ac 2 -c:a pcm_f32le "$g.a.wav"
      echo "file '$(basename "$g").a.wav'" >> "$D/sub_a.txt"
    done
    if [ "$S" -gt 1 ]; then
      ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$D/sub_v.txt" -f concat -safe 0 -i "$D/sub_a.txt" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k "$f.tmp.mp4"
      rm -f "$f".s*.mp4 "$f".s*.mp4.a.wav
    else
      rm -f "$f.tmp.mp4.a.wav"
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
# quadro i em i / FPS (na 1ª execução, a parte montada de pedaços entrou com +42 ms; corrigir_ts_video.py conserta
# sem recodificar e para com erro se não conseguir)
python3 -I rev3/corrigir_ts_video.py "$D/video.mp4" "$FPS" "$TOTAL"
python3 -I rev3/mixar_rev3.py --saida "$D/mix.wav" --sfx "$D/sfx.wav" | tail -1
python3 -I rev3/corrigir_pico_aac.py "$D/mix.wav" "$D/video.mp4" "$SAIDA" 192k
rm -f "$D/video.mp4" "$D"/f_*.mp4 "$D"/f_*.mp4.a.wav  # partes só saem com o arquivo final pronto
ffmpeg -nostdin -hide_banner -i "$SAIDA" -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A15 Summary | grep -E "I:|Peak:"
ffprobe -v error -show_entries stream=codec_type,codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,duration,bit_rate -of compact "$SAIDA"
echo "FIM $(date +%H:%M)"
