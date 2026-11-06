#!/bin/bash
# Render da REV3 (de reels/ams-yt). Precisa do proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# e de `python rev3/montar_rev3.py` + `python rev3/mixar_rev3.py --saida _tmp/mix_base.wav` (gera o cache da mixagem).
#
#   bash rev3/renderizar_rev3.sh trechos [nomes]  trechos de aprovação (gancho, hotel, mccrispy, fechamento; padrão: todos)
#   bash rev3/renderizar_rev3.sh previa    vídeo inteiro em 720p, em 8 partes, juntadas e recomprimidas em ~1 Mbps
#   bash rev3/renderizar_rev3.sh final1080 vídeo inteiro em 1080p, do proxy (CRF 19, até 12 Mbps), em 16 partes
#   bash rev3/renderizar_rev3.sh final4k   vídeo inteiro em 4K, da fonte (CRF 19, até 20 Mbps, ~5 GB), em 16 partes
#
# A imagem sai do Remotion (H.264, CRF 20) e o som da mixagem (`rev3/finalizar_rev3.py`: AAC 192 kbps e medida
# de loudness e pico verdadeiro no arquivo exportado).
set -euo pipefail
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
ESCALA=0.6666666666666666  # 1280 × 720
export BUNDLE_DIR="$RAIZ/_tmp/bundle"
rm -rf "$BUNDLE_DIR"  # o bundle é refeito a cada chamada: um bundle velho renderiza o código velho do Remotion

render() {  # $1 saída, $2 quadro inicial, $3 quadro final [, $4 props, $5 escala]
  # para no primeiro erro (uma parte que falha não pode deixar o laço seguir) e só grava a saída quando o render
  # termina: parte pela metade nunca passa por pronta. O Remotion copia o vídeo-fonte para o /tmp a cada render;
  # a cópia de um render interrompido fica lá, então limpo antes de cada parte.
  rm -rf /tmp/remotion-v*-assets* 2>/dev/null || true
  local log="$RAIZ/_tmp/render_parte.log"
  if ! (cd ../../design-system/remotion && node scripts/videolongo.mjs "${4:-$RAIZ/rev3/props_rev3.json}" "$RAIZ/public" trecho "$1.tmp.mp4" "$2" "$3" "${5:-$ESCALA}" > "$log" 2>&1); then
    grep -v "%$" "$log" | tail -20
    exit 1
  fi
  mv "$1.tmp.mp4" "$1"
  echo "ok $1"
}

juntar() {  # $1 lista de partes, $2 vídeo de saída, $3 som do render (wav); depois de $3: opções de vídeo do ffmpeg
  # imagem e som juntados à parte: cada parte do Remotion tem o áudio 7 ms mais longo que a imagem, e o concat de
  # arquivos inteiros atrasaria a imagem a cada emenda (2 quadros a mais no vídeo inteiro da prévia)
  local lista=$1 saida=$2 som=$3; shift 3
  : > _tmp/juntar_v.txt; : > _tmp/juntar_a.txt
  while read -r _ f; do
    f=${f//\'/}
    q=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$f")
    ffmpeg -nostdin -v error -y -i "$f" -map 0:v -c copy "$f.v.mp4"
    ffmpeg -nostdin -v error -y -i "$f" -map 0:a -af "apad,atrim=end=$(python3 -c "print($q / 24)")" -ar 48000 -ac 2 -c:a pcm_f32le "$f.a.wav"
    echo "file '$f.v.mp4'" >> _tmp/juntar_v.txt
    echo "file '$f.a.wav'" >> _tmp/juntar_a.txt
  done < "$lista"
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/juntar_v.txt "$@" -an -movflags +faststart "$saida"
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/juntar_a.txt -c:a pcm_f32le "$som"
  while read -r _ f; do f=${f//\'/}; rm -f "$f.v.mp4" "$f.a.wav"; done < "$lista"
}

juntar_leve() {  # $1 lista de partes, $2 vídeo de saída, $3 som do render (wav)
  # como o juntar(), mas sem copiar a imagem de cada parte (no 4K as cópias não cabem no disco): a lista do concat
  # leva a duração exata da imagem de cada parte (`duration`), e a parte seguinte começa ali, não no fim do áudio
  # (7 ms mais longo). As partes só são apagadas depois de conferir que o vídeo juntado tem todos os quadros.
  local lista=$1 saida=$2 som=$3 total=0
  : > _tmp/juntar_v.txt; : > _tmp/juntar_a.txt
  while read -r _ f; do
    f=${f//\'/}
    q=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$f")
    total=$((total + q))
    ffmpeg -nostdin -v error -y -i "$f" -map 0:a -af "apad,atrim=end=$(python3 -c "print($q / 24)")" -ar 48000 -ac 2 -c:a pcm_f32le "$f.a.wav"
    printf "file '%s'\nduration %s\n" "$f" "$(python3 -c "print($q / 24)")" >> _tmp/juntar_v.txt
    echo "file '$f.a.wav'" >> _tmp/juntar_a.txt
  done < "$lista"
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/juntar_v.txt -map 0:v -c copy -movflags +faststart "$saida"
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/juntar_a.txt -c:a pcm_f32le "$som"
  local q_saida
  q_saida=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$saida")
  [ "$q_saida" -eq "$total" ] || { echo "juntar_leve: $q_saida quadros no vídeo juntado, esperado $total"; exit 1; }
  while read -r _ f; do f=${f//\'/}; rm -f "$f" "$f.a.wav"; done < "$lista"
}

case "${1:-}" in
  trechos)
    shift
    QUAIS="${*:-gancho hotel mccrispy fechamento}"
    for t in "gancho 0 815" "hotel 1296 1703" "mccrispy 18960 19439" "fechamento 45000 47502"; do
      set -- $t
      [[ " $QUAIS " == *" $1 "* ]] || continue
      render "$RAIZ/_tmp/r_$1.mp4" "$2" "$3"
      python3 rev3/finalizar_rev3.py "_tmp/r_$1.mp4" "$(python3 -c "print($2 * 1000 / 24)")" "rev3/rev3_$1.mp4"
    done
    ;;
  juntar)  # só junta as partes já prontas da prévia e finaliza (refaz o fim do "previa" sem renderizar)
    juntar _tmp/partes.txt _tmp/previa_video.mp4 _tmp/previa_sfx.wav -c:v libx264 -preset veryfast -crf 30 -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p
    python3 rev3/finalizar_rev3.py _tmp/previa_video.mp4 0 rev3/rev3_previa_720p.mp4 _tmp/previa_sfx.wav
    ;;
  previa)
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/linha_do_tempo_rev3.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=8
    : > _tmp/partes.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/p_$i.mp4" ] || render "$RAIZ/_tmp/p_$i.mp4" "$a" "$b"
      echo "file '$RAIZ/_tmp/p_$i.mp4'" >> _tmp/partes.txt
    done
    # junta as partes já recomprimindo em ~1 Mbps (o grão do DS faz o CRF 20 passar de 2 GB no vídeo inteiro)
    juntar _tmp/partes.txt _tmp/previa_video.mp4 _tmp/previa_sfx.wav -c:v libx264 -preset veryfast -crf 30 -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p
    python3 rev3/finalizar_rev3.py _tmp/previa_video.mp4 0 rev3/rev3_previa_720p.mp4 _tmp/previa_sfx.wav
    ;;
  final1080)
    # 1920 × 1080 do proxy (o proxy já é 1080p: escala 1), x264 CRF 19 com teto de 12 Mbps (YouTube recomenda 8 Mbps
    # para 1080p a 24 qps; o teto segura o grão do DS), em 16 partes (cada uma refeita só se faltar)
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/linha_do_tempo_rev3.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=16
    : > _tmp/partes1080.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/h_$i.mp4" ] || X264_PRESET=fast CRF=19 MAXRATE=12M render "$RAIZ/_tmp/h_$i.mp4" "$a" "$b" "$RAIZ/rev3/props_rev3.json" 1
      echo "file '$RAIZ/_tmp/h_$i.mp4'" >> _tmp/partes1080.txt
    done
    juntar _tmp/partes1080.txt _tmp/final1080_video.mp4 _tmp/final1080_sfx.wav -c copy
    python3 rev3/finalizar_rev3.py _tmp/final1080_video.mp4 0 _tmp/rev3_final_1080p.mp4 _tmp/final1080_sfx.wav
    ;;
  final4k)
    # 3840 × 2160 lendo direto a fonte 4K (HEVC 10 bits; o Remotion decodifica pelo <OffthreadVideo>), x264 fast
    # CRF 19 com teto de 20 Mbps, em 16 partes (cada uma refeita só se faltar). O teto é o que cabe no disco desta
    # sessão (partes + vídeo juntado ≈ 2 × 5 GB, mais ~4 GB de WAV da mixagem); o YouTube recomenda 35–45 Mbps em
    # H.264, mas recodifica tudo (o 4K dele sai em VP9/AV1 abaixo disso).
    ln -sf "$RAIZ/fonte/1016_sem_musica.mp4" _tmp/servir/fonte4k.mp4
    python3 -c "
import json; p = json.load(open('rev3/props_rev3.json')); p['video'] = 'http://127.0.0.1:8787/fonte4k.mp4'
json.dump(p, open('_tmp/props_rev3_4k.json', 'w'), ensure_ascii=False)"
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev3/linha_do_tempo_rev3.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=16
    : > _tmp/partes4k.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/f_$i.mp4" ] || CONCURRENCY=3 OFFTHREAD_CACHE_MB=1500 X264_PRESET=fast CRF=19 MAXRATE=20M render "$RAIZ/_tmp/f_$i.mp4" "$a" "$b" "$RAIZ/_tmp/props_rev3_4k.json" 2
      echo "file '$RAIZ/_tmp/f_$i.mp4'" >> _tmp/partes4k.txt
    done
    rm -rf /tmp/remotion-v*-assets* 2>/dev/null || true  # a cópia da fonte 4K (4,7 GB) não serve mais
    juntar_leve _tmp/partes4k.txt _tmp/final4k_video.mp4 _tmp/final4k_sfx.wav
    python3 rev3/finalizar_rev3.py _tmp/final4k_video.mp4 0 _tmp/rev3_final_4k.mp4 _tmp/final4k_sfx.wav
    rm -f _tmp/final4k_video.mp4
    ;;
  *)
    echo "uso: bash rev3/renderizar_rev3.sh trechos|previa|juntar|final1080|final4k"; exit 1 ;;
esac
