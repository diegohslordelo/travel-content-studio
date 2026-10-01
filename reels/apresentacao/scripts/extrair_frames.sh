#!/bin/bash
# Extrai 1 frame a cada 2 s do original (HDR HLG -> SDR Rec.709, tone mapping Hable), 480x270.
# Funciona enquanto o arquivo ainda está baixando: processa blocos de 120 s só quando
# há dados suficientes e confere a contagem de frames de cada bloco.
#
# Uso: extrair_frames.sh ARQUIVO_FINAL ARQUIVO_PARCIAL_GLOB DURACAO_S TAMANHO_TOTAL_BYTES PASTA_SAIDA
set -u
FINAL="$1"; PARCIAL_GLOB="$2"; DUR="$3"; TOTAL="$4"; OUT="$5"
mkdir -p "$OUT"
TM="zscale=w=480:h=270:tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=pc,format=yuvj420p"
BLOCO=120
a=0
dur_int=${DUR%.*}
parciais=()
while [ "$a" -le "$dur_int" ]; do
  if [ -f "$FINAL" ]; then
    SRC="$FINAL"; seguro=999999; completo=1
  else
    SRC=$(ls $PARCIAL_GLOB 2>/dev/null | head -1)
    if [ -z "$SRC" ]; then sleep 5; continue; fi
    bytes=$(stat -c %s "$SRC")
    # tempo estimado já baixado (taxa média do arquivo), com margem de 90 s
    seguro=$(python3 -c "print(int($bytes / ($TOTAL / $DUR) - 90))")
    completo=0
  fi
  b=$((a + BLOCO))
  if [ "$completo" -eq 1 ] || [ "$b" -le "$seguro" ]; then
    esperado=$((BLOCO / 2))  # só é conferido em blocos inteiros feitos com o arquivo parcial
    ffmpeg -v error -y -ss "$a" -t "$BLOCO" -i "$SRC" -an -vf "fps=1/2,$TM" -q:v 3 \
      -start_number $((a / 2 + 1)) "$OUT/f_%05d.jpg"
    n=0
    for ((k = a / 2 + 1; k < a / 2 + 1 + BLOCO / 2; k++)); do
      [ -f "$(printf "$OUT/f_%05d.jpg" $k)" ] && n=$((n + 1))
    done
    if [ "$n" -lt "$esperado" ] && [ "$completo" -eq 0 ]; then
      echo "$(date +%T) bloco ${a}s incompleto ($n/$esperado), aguardando mais dados"
      for ((k = a / 2 + 1; k < a / 2 + 1 + BLOCO / 2; k++)); do rm -f "$(printf "$OUT/f_%05d.jpg" $k)"; done
      sleep 30
      continue
    fi
    [ "$completo" -eq 0 ] && parciais+=("$a")
    echo "$(date +%T) bloco ${a}-${b}s ok ($n frames) $([ $completo -eq 1 ] && echo '[arquivo completo]' || echo '[arquivo parcial]')"
    a=$b
  else
    sleep 20
  fi
done
# Reverifica os 2 últimos frames de cada bloco feito com o arquivo parcial.
while [ ! -f "$FINAL" ]; do sleep 10; done
for a in "${parciais[@]}"; do
  for t in $((a + BLOCO - 4)) $((a + BLOCO - 2)); do
    ffmpeg -v error -y -ss "$t" -i "$FINAL" -an -frames:v 1 -vf "$TM" -q:v 3 "$(printf "$OUT/f_%05d.jpg" $((t / 2 + 1)))"
  done
done
echo "$(date +%T) FIM: $(ls "$OUT"/f_*.jpg | wc -l) frames"
