#!/usr/bin/env bash
# Prévias leves (960 × 540) dos pontos-chave da REV1 (de reels/bru-yt). Precisa do proxy servido em 127.0.0.1:8787:
#   node ../../design-system/remotion/scripts/servir.mjs _tmp/servir 8787
# Uso: bash rev1/previas_rev1.sh [nome ...]   (sem nome: todas). Cada prévia: render do Remotion (imagem + efeitos
# sonoros) → mixagem da REV1 no mesmo trecho (voz, música, efeitos, −14 LUFS) → MP4 (H.264 CRF 27 + AAC 160 kbps).
set -euo pipefail
cd "$(dirname "$0")/.."
FPS=30
RM=../../design-system/remotion
declare -A INI FIM PROPS
# nome            início (ms)  fim (ms)   props (guia = texto das narrações na tela)
INI[gancho]=0;          FIM[gancho]=36000;     PROPS[gancho]=rev1/props_rev1_guia.json
INI[metro]=55500;       FIM[metro]=78500;      PROPS[metro]=rev1/props_rev1.json
INI[zinneke]=139500;    FIM[zinneke]=172000;   PROPS[zinneke]=rev1/props_rev1.json
INI[fritland]=200000;   FIM[fritland]=255000;  PROPS[fritland]=rev1/props_rev1.json
INI[hotel]=307500;      FIM[hotel]=336000;     PROPS[hotel]=rev1/props_rev1_guia.json
INI[waffle]=346000;     FIM[waffle]=397000;    PROPS[waffle]=rev1/props_rev1.json
INI[chocolate]=465000;  FIM[chocolate]=482000; PROPS[chocolate]=rev1/props_rev1.json
INI[manneken]=487500;   FIM[manneken]=560000;  PROPS[manneken]=rev1/props_rev1.json
INI[merveilleux]=683000; FIM[merveilleux]=725000; PROPS[merveilleux]=rev1/props_rev1.json
INI[spago]=835000;      FIM[spago]=847000;     PROPS[spago]=rev1/props_rev1.json
INI[fechamento]=860000; FIM[fechamento]=930400; PROPS[fechamento]=rev1/props_rev1_guia.json
ORDEM=(gancho metro zinneke fritland hotel waffle chocolate manneken merveilleux spago fechamento)
[ $# -gt 0 ] && ORDEM=("$@")
mkdir -p _tmp/previas rev1/previas
for n in "${ORDEM[@]}"; do
  q0=$(( INI[$n] * FPS / 1000 )); q1=$(( FIM[$n] * FPS / 1000 - 1 ))
  echo "== $n: quadros $q0–$q1"
  # o Remotion copia o proxy para o temporário a cada render: temporário próprio do projeto, limpo a cada prévia
  rm -rf _tmp/rtmp && mkdir -p _tmp/rtmp
  if [ ! -s "_tmp/previas/$n.render.mp4" ]; then
    (cd "$RM" && TMPDIR="$OLDPWD/_tmp/rtmp" CRF=24 X264_PRESET=veryfast node scripts/videolongo.mjs "../../reels/bru-yt/${PROPS[$n]}" ../../reels/bru-yt/public trecho "../../reels/bru-yt/_tmp/previas/$n.render.mp4" "$q0" "$q1" 0.5) 2>&1 | grep -v -i "memory\|docker" | tail -2
  fi
  ffmpeg -nostdin -v error -y -i "_tmp/previas/$n.render.mp4" -map 0:a -ar 48000 -ac 2 -c:a pcm_f32le "_tmp/previas/$n.sfx.wav"
  ini_ms=$(python3 -c "print($q0 * 1000 / $FPS)"); fim_ms=$(python3 -c "print(($q1 + 1) * 1000 / $FPS)")
  python3 -I rev1/mixar_rev1.py --saida "_tmp/previas/$n.mix.wav" --sfx "_tmp/previas/$n.sfx.wav" --de "$ini_ms" --ate "$fim_ms" | tail -1
  ffmpeg -nostdin -v error -y -i "_tmp/previas/$n.render.mp4" -i "_tmp/previas/$n.mix.wav" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 160k -shortest -movflags +faststart "rev1/previas/rev1_$n.mp4"
  ls -la "rev1/previas/rev1_$n.mp4" | awk '{print $5, $9}'
done
