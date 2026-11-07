#!/usr/bin/env bash
# Arquivo final da REV4 (de reels/bru-yt): a imagem 4K da REV3 (não muda: mesmos cortes, objetos e timestamps) com o
# som novo da REV4. Não renderiza nada: junta a mixagem da REV4 (rev4/mixar_rev4.py) com os efeitos do Remotion do
# render 4K da REV3 (_tmp/final4k_rev3/sfx.wav), corrige o pico pós-AAC (AAC 192 kbps 48 kHz) e copia a imagem de
# _tmp/rev3_final_4k.mp4. Mede no arquivo exportado (padrão de áudio, 11.3).
# Precisa de: _tmp/rev3_final_4k.mp4 e _tmp/final4k_rev3/sfx.wav (rev3/renderizar_final4k_rev3.sh).
set -euo pipefail
cd "$(dirname "$0")/.."
D=_tmp/final4k_rev4
SAIDA=_tmp/rev4_final_4k.mp4
mkdir -p "$D"
python3 -I rev4/mixar_rev4.py --saida "$D/mix.wav" --sfx _tmp/final4k_rev3/sfx.wav | tail -1
python3 -I rev4/corrigir_pico_aac.py "$D/mix.wav" _tmp/rev3_final_4k.mp4 "$SAIDA" 192k | tail -2
python3 -I rev4/corrigir_ts_video.py "$SAIDA" 30 28508
ffmpeg -nostdin -hide_banner -i "$SAIDA" -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary | grep -E "I:|LRA:|Peak:"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration,bit_rate -of compact "$SAIDA"
ffmpeg -nostdin -v error -i "$SAIDA" -map 0:a -f null - && echo "som decodificado sem erro"
md5sum "$SAIDA"
