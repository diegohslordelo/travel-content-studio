#!/bin/bash
# Baixa do Drive (Youtube/Amsterdam) os clipes listados em ids_drive.tsv que ainda não estão em fonte/clipes/.
# Uso (de dentro de reels/ams-custo/): bash scripts/baixar.sh
cd "$(dirname "$0")/.." || exit 1
while IFS=$'\t' read -r nome id; do
  [ -s "fonte/clipes/$nome" ] && continue
  curl -sSL -o "fonte/clipes/$nome" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t" &
  while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 0.3; done
done < ids_drive.tsv
wait
