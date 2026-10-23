#!/bin/bash
# Render da REV2 (de reels/ams-yt). Precisa do proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# e de `python rev2/montar_rev2.py` + `python rev2/mixar_rev2.py --saida _tmp/mix_base.wav` (gera o cache da mixagem).
#
#   bash rev2/renderizar_rev2.sh trechos [nomes]  trechos de aprovação (gancho, hotel, mccrispy, fechamento; padrão: todos)
#   bash rev2/renderizar_rev2.sh previa    vídeo inteiro em 720p, em 8 partes, juntadas sem recodificar
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

render() {  # $1 saída, $2 quadro inicial, $3 quadro final
  (cd ../../design-system/remotion && node scripts/videolongo.mjs "$RAIZ/rev2/props_rev2.json" "$RAIZ/public" trecho "$1" "$2" "$3" "$ESCALA" 2>&1 | grep -E "^ok|Error|error" || true)
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
  previa)
    TOTAL=$(python3 -c "import json; print(round(json.load(open('rev2/linha_do_tempo_rev2.json'))['duracao_ms'] * 24 / 1000))")
    PARTES=8
    : > _tmp/partes.txt
    for i in $(seq 0 $((PARTES - 1))); do
      a=$((TOTAL * i / PARTES)); b=$((TOTAL * (i + 1) / PARTES - 1))
      [ -s "_tmp/p_$i.mp4" ] || render "$RAIZ/_tmp/p_$i.mp4" "$a" "$b"
      echo "file '$RAIZ/_tmp/p_$i.mp4'" >> _tmp/partes.txt
    done
    ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/partes.txt -c copy _tmp/previa_video.mp4
    python3 rev2/finalizar_rev2.py _tmp/previa_video.mp4 0 _tmp/previa_mix.mp4
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
      if [ ! -s "_tmp/f_$i.mp4" ]; then
        (cd ../../design-system/remotion && X264_PRESET=veryfast CRF=20 node scripts/videolongo.mjs "$RAIZ/_tmp/props_rev2_4k.json" "$RAIZ/public" trecho "$RAIZ/_tmp/f_$i.mp4" "$a" "$b" 2 2>&1 | grep -E "^ok|Error|error" || true)
      fi
      echo "file '$RAIZ/_tmp/f_$i.mp4'" >> _tmp/partes4k.txt
    done
    ffmpeg -nostdin -v error -y -f concat -safe 0 -i _tmp/partes4k.txt -c copy _tmp/final4k_video.mp4
    python3 rev2/finalizar_rev2.py _tmp/final4k_video.mp4 0 _tmp/rev2_final_4k.mp4
    ;;
  *)
    echo "uso: bash rev2/renderizar_rev2.sh trechos|previa|final4k"; exit 1 ;;
esac
