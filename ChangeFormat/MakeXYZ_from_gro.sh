#!/bin/bash

for fname in $(ls .); do
  if [[ "${fname##*.}" == "gro" ]]; then
    xyzFile="${fname/gro/xyz}"
    awk -f gro2xyz.awk $fname > $xyzFile
  fi
done

