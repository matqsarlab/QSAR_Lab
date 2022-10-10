#!/bin/bash

for fname in $(ls .); do
  if [[ "${fname##*.}" == "gro" ]]; then
    xyzFile="${fname/gro/xyz}"
    awk -f gro2xyz_noH2O.awk $fname > "no_water_"$xyzFile
  fi
done

for fname in $(ls .); do
  if [[ "${fname##*.}" == "xyz" ]]; then
    LineNum=$(wc -l $fname | awk '{print $1}')
    LineNum=$(($LineNum-2))
    # awk -i '$0 = FNR==1 ? replace : $0' replace="$z" $fname
    sed -i "" "1s/.*/$LineNum/" $fname
  fi
done
