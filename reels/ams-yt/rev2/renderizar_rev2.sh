#!/bin/bash
# Render da REV2 (de reels/ams-yt). Precisa do proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# e de `python rev2/montar_rev2.py` + `python rev2/mixar_rev2.py --saida _tmp/mix_base.wav` (gera o cache da mixagem).
#
#   bash rev2/renderizar_rev2.sh trechos [nomes]  trechos de aprovação (gancho, hotel, mccrispy, fechamento; padrão: todos)
#   bash rev2/renderizar_rev2.sh previa    vídeo inteiro em 720p, em 8 partes, juntadas e recomprimidas em ~1 Mbps
#   bash rev2/renderizar_rev2.sh final4k   vídeo inteiro em 4K, da fonte (4 a 6 h em 4 núcleos; ~7 GB)
#
# A imagem sai do Remotion (H.264, CRF 20) e o som da mixagem (`rev2/finalizar_rev2.py`: AAC 192 kbps e medida
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
  if ! (cd ../../design-system/remotion && node scripts/videolongo.mjs "${4:-$RAIZ/rev2/props_rev2.json}" "$RAIZ/public" trecho "$1.tmp.mp4" "$2" "$3" "${5:-$ESCALA}" > "$log" 2>&1); then
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

case "${1:-}" in
  trechos)
    shift
    QUAIS="${*:-gancho hotel mccrispy fechamento}"
    for t in "gancho 0 815" "hotel 1296 1703" "mccrispy 18960 19439" "fechamento 45000 47502"; do
      set -- $t
      [[ " $QUAIS " == *" $1 "* ]] || continue
      render "$RAIZ/_tmp/r_$1.mp4" "$2" "$3"
      python3 rev2/finalizar_rev2.py "_tmp/r_$1.mp4" "$(python3 -c "print($2 * 1000 / 24)")" "rev2/rev2_$1.mp4"
    done
    ;;
  juntar)  # só junta as partes já prontas da prévia e finaliza (refaz o fim do "previa" sem renderizar)
    juntar _tmp/partes.txt _tmp/previa_video.mp4 _tmp/previa_sfx.wav -c:v libx264 -preset veryfast -crf 30 -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p
    python3 rev2/finalizar_rev2.py _tmp/previa_video.mp4 0 rev2/rev2_previa_720p.mp4 _tmp/previa_sfx.wav
    ;;
  previa)
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev2/linha_do_tempo_rev2.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=8
    : > _tmp/partes.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/p_$i.mp4" ] || render "$RAIZ/_tmp/p_$i.mp4" "$a" "$b"
      echo "file '$RAIZ/_tmp/p_$i.mp4'" >> _tmp/partes.txt
    done
    # junta as partes já recomprimindo em ~1 Mbps (o grão do DS faz o CRF 20 passar de 2 GB no vídeo inteiro)
    juntar _tmp/partes.txt _tmp/previa_video.mp4 _tmp/previa_sfx.wav -c:v libx264 -preset veryfast -crf 30 -maxrate 1000k -bufsize 2000k -pix_fmt yuv420p
    python3 rev2/finalizar_rev2.py _tmp/previa_video.mp4 0 rev2/rev2_previa_720p.mp4 _tmp/previa_sfx.wav
    ;;
  final4k)
    # 3840 × 2160 lendo direto a fonte 4K (HEVC 10 bits; o Remotion decodifica pelo <OffthreadVideo>), x264 veryfast
    # CRF 20, em 16 partes (cada uma refeita só se faltar). Espaço: ~7 GB de partes + ~7 GB do arquivo final.
    ln -sf "$RAIZ/fonte/1016_sem_musica.mp4" _tmp/servir/fonte4k.mp4
    python3 -c "
import json; p = json.load(open('rev2/props_rev2.json')); p['video'] = 'http://127.0.0.1:8787/fonte4k.mp4'
json.dump(p, open('_tmp/props_rev2_4k.json', 'w'), ensure_ascii=False)"
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev2/linha_do_tempo_rev2.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=16
    : > _tmp/partes4k.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/f_$i.mp4" ] || X264_PRESET=veryfast CRF=20 render "$RAIZ/_tmp/f_$i.mp4" "$a" "$b" "$RAIZ/_tmp/props_rev2_4k.json" 2
      echo "file '$RAIZ/_tmp/f_$i.mp4'" >> _tmp/partes4k.txt
    done
    juntar _tmp/partes4k.txt _tmp/final4k_video.mp4 _tmp/final4k_sfx.wav -c copy
    python3 rev2/finalizar_rev2.py _tmp/final4k_video.mp4 0 _tmp/rev2_final_4k.mp4 _tmp/final4k_sfx.wav
    ;;
  *)
    echo "uso: bash rev2/renderizar_rev2.sh trechos|previa|juntar|final4k"; exit 1 ;;
esac
