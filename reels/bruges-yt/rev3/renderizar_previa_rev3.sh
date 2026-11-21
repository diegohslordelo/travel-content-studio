#!/usr/bin/env bash
# Prévia leve (960 × 540) do vídeo inteiro da REV3 (vlog de Bruges), para o Diego aprovar cortes e animações.
# Roda de reels/bruges-yt, com o proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# Uso: bash rev3/renderizar_previa_rev3.sh
# Renderiza em PARTES partes (cada parte só é refeita se faltar: um reinício do container custa no máximo uma parte),
# junta a imagem sem recodificar e põe o som da prévia (rev3/musica_rev3.py + rev3/mixar_previa_rev3.py: voz decupada,
# efeitos e música; sem keen). Saída: rev3/previas/rev3_previa_540p.mp4
set -euo pipefail
cd "$(dirname "$0")/.."
PARTES=${PARTES:-8}
RM=../../design-system/remotion
DIR=_tmp/previa_rev3
mkdir -p "$DIR" rev3/previas _tmp/rtmp
TOTAL=$(python3 -c "import json; p=json.load(open('rev3/props_rev3.json')); print(round(p['duracao']*p['fps']/1000))")
echo "quadros: $TOTAL em $PARTES partes"
export BUNDLE_DIR="$PWD/_tmp/bundle_rev3"
for i in $(seq 0 $((PARTES - 1))); do
  a=$(( TOTAL * i / PARTES )); b=$(( TOTAL * (i + 1) / PARTES - 1 ))
  out="$DIR/parte_$i.mp4"
  [ -s "$out" ] && { echo "parte $i pronta"; continue; }
  echo "== parte $i: quadros $a–$b"
  rm -rf _tmp/rtmp/* /tmp/remotion-v*-assets* 2>/dev/null || true
  (cd "$RM" && TMPDIR="$OLDPWD/_tmp/rtmp" CRF=26 X264_PRESET=veryfast node scripts/videolongo.mjs ../../reels/bruges-yt/rev3/props_rev3.json ../../reels/bruges-yt/public trecho "../../reels/bruges-yt/$out.tmp.mp4" "$a" "$b" 0.5) 2>&1 | grep -v -i "memory\|docker" | tail -1
  mv "$out.tmp.mp4" "$out"
done
# imagem: junta sem recodificar; efeitos: cada parte cortada no tamanho exato da imagem
: > "$DIR/lista.txt"
for i in $(seq 0 $((PARTES - 1))); do echo "file 'parte_$i.mp4'" >> "$DIR/lista.txt"; done
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$DIR/lista.txt" -map 0:v -c copy "$DIR/imagem.mp4"
python3 -I - "$DIR" "$PARTES" <<'EOF'
import subprocess, sys, json
import numpy as np, soundfile as sf
d, n = sys.argv[1], int(sys.argv[2])
fps = json.load(open("rev3/props_rev3.json"))["fps"]
pedacos = []
for i in range(n):
    q = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", f"{d}/parte_{i}.mp4"]).decode().strip().strip(","))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{d}/parte_{i}.mp4", "-map", "0:a", "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", f"{d}/sfx_{i}.wav"], check=True)
    x, sr = sf.read(f"{d}/sfx_{i}.wav", dtype="float32", always_2d=True)
    alvo = round(q * sr / fps)
    x = x[:alvo] if len(x) >= alvo else np.vstack([x, np.zeros((alvo - len(x), 2), np.float32)])
    pedacos.append(x)
sf.write(f"{d}/sfx.wav", np.vstack(pedacos), 48000, subtype="FLOAT")
EOF
python3 -I rev3/musica_rev3.py
python3 -I rev3/mixar_previa_rev3.py --sfx "$DIR/sfx.wav" --saida "$DIR/mix.wav"
# o pico dos efeitos segura o ganho da mixagem: +6,5 dB e limitador a −1 dBFS (≈ −16,6 LUFS); imagem recomprimida (CRF 31)
ffmpeg -nostdin -v error -y -i "$DIR/mix.wav" -af "volume=6.5dB,alimiter=limit=0.89:attack=5:release=60:level=disabled" -c:a pcm_f32le "$DIR/mix_lim.wav"
ffmpeg -nostdin -v error -y -i "$DIR/imagem.mp4" -i "$DIR/mix_lim.wav" -map 0:v -map 1:a -c:v libx264 -preset faster -crf 31 -c:a aac -b:a 160k -shortest -movflags +faststart rev3/previas/rev3_previa_540p.mp4
ls -la rev3/previas/rev3_previa_540p.mp4
