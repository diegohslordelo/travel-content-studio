#!/usr/bin/env bash
# Render FINAL da REV5 (vlog de Bruges) em 4K, lendo direto a fonte 4K (HEVC 10 bits). Pedido do Diego (21/11/2026):
# "renderize tudo na maior qualidade possível".
#
# Roda de reels/bruges-yt, com a pasta _tmp/servir servida em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
#   python -I rev5/montar_rev5.py && bash rev5/renderizar_final_rev5.sh
# Depois: python -I rev5/finalizar_rev5.py (mixagem final + AAC + medidas).
#
# Qualidade: 3840 × 2160 (escala 2 da composição 1920 × 1080), cada quadro em JPEG 100 (o padrão do Remotion é 80),
# x264 preset medium, CRF 17 com teto de 45 Mbps (o YouTube recomenda 35–45 Mbps para subir 4K a 24 qps em H.264; no
# teste, o CRF 17 ficou em ~29 Mbps). Cores conferidas contra a fonte (diferença média < 2/255 por canal).
# Em PARTES partes (cada uma só é refeita se faltar: um reinício do container custa no máximo uma parte). Junta só a
# IMAGEM das partes, sem recodificar (REV4: com o áudio junto, o concat atrasava a imagem a cada emenda); o som dos
# efeitos de cada parte é cortado no tamanho exato da imagem dela e juntado à parte.
# Saídas: _tmp/final_rev5/imagem.mp4 (só imagem) e _tmp/final_rev5/sfx.wav (efeitos do Remotion, 48 kHz).
set -euo pipefail
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
PARTES=${PARTES:-16}
RM=../../design-system/remotion
DIR=_tmp/final_rev5
mkdir -p "$DIR" _tmp/rtmp
ln -sf "$RAIZ/fonte/1120.mp4" _tmp/servir/fonte4k.mp4
python3 -c "
import json; p = json.load(open('rev5/props_rev5.json')); p['video'] = 'http://127.0.0.1:8787/fonte4k.mp4'
json.dump(p, open('_tmp/props_rev5_4k.json', 'w'), ensure_ascii=False)"
TOTAL=$(python3 -c "import json; p=json.load(open('rev5/props_rev5.json')); print(round(p['duracao']*p['fps']/1000))")
echo "quadros: $TOTAL em $PARTES partes"
export BUNDLE_DIR="$RAIZ/_tmp/bundle_rev5"
for i in $(seq 0 $((PARTES - 1))); do
  a=$(( TOTAL * i / PARTES )); b=$(( TOTAL * (i + 1) / PARTES - 1 ))
  out="$DIR/parte_$i.mp4"
  [ -s "$out" ] && { echo "parte $i pronta"; continue; }
  echo "== $(date +%H:%M:%S) parte $i: quadros $a–$b"
  rm -rf _tmp/rtmp/* /tmp/remotion-v*-assets* 2>/dev/null || true
  log="$RAIZ/_tmp/render_parte_rev5.log"
  if ! (cd "$RM" && TMPDIR="$RAIZ/_tmp/rtmp" CONCURRENCY=4 OFFTHREAD_CACHE_MB=2000 X264_PRESET=medium CRF=17 MAXRATE=45M JPEG_QUALITY=100 \
        node scripts/videolongo.mjs "$RAIZ/_tmp/props_rev5_4k.json" "$RAIZ/public" trecho "$RAIZ/$out.tmp.mp4" "$a" "$b" 2 > "$log" 2>&1); then
    grep -v "%$" "$log" | tail -20
    exit 1
  fi
  q=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nw=1:nk=1 "$out.tmp.mp4" | tr -d ',')
  [ "$q" -eq $((b - a + 1)) ] || { echo "parte $i com $q quadros (esperado $((b - a + 1)))"; exit 1; }
  mv "$out.tmp.mp4" "$out"
done
rm -rf /tmp/remotion-v*-assets* 2>/dev/null || true
: > "$DIR/lista.txt"
for i in $(seq 0 $((PARTES - 1))); do
  ffmpeg -nostdin -v error -y -i "$DIR/parte_$i.mp4" -map 0:v -c copy "$DIR/parte_${i}_v.mp4"
  echo "file 'parte_${i}_v.mp4'" >> "$DIR/lista.txt"
done
ffmpeg -nostdin -v error -y -f concat -safe 0 -i "$DIR/lista.txt" -map 0:v -c copy -movflags +faststart "$DIR/imagem.mp4"
python3 -I - "$DIR" "$PARTES" "$TOTAL" <<'EOF'
import subprocess, sys
import numpy as np, soundfile as sf
d, n, total = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
pedacos, soma = [], 0
for i in range(n):
    q = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", f"{d}/parte_{i}.mp4"]).decode().strip().strip(","))
    soma += q
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{d}/parte_{i}.mp4", "-map", "0:a", "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", f"{d}/sfx_{i}.wav"], check=True)
    x, sr = sf.read(f"{d}/sfx_{i}.wav", dtype="float32", always_2d=True)
    alvo = round(q * sr / 24)
    x = x[:alvo] if len(x) >= alvo else np.vstack([x, np.zeros((alvo - len(x), 2), np.float32)])
    pedacos.append(x)
q = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", f"{d}/imagem.mp4"]).decode().strip().strip(","))
assert soma == total == q, f"quadros: partes {soma}, juntado {q}, esperado {total}"
sf.write(f"{d}/sfx.wav", np.vstack(pedacos), 48000, subtype="FLOAT")
print(f"ok: {q} quadros = {q / 24:.3f} s; efeitos {sum(len(p) for p in pedacos) / 48000:.3f} s")
EOF
rm -f "$DIR"/parte_*_v.mp4 "$DIR"/sfx_*.wav
echo "$(date +%H:%M:%S) render pronto"
