#!/bin/bash

DIR=$(ls -d */)
NM=$(pwd)

for i in $DIR; do
  if [[ ! -f "$i/tryton.sh" ]]; then
    echo $i"tryton.sh" is writting:
    cp tryton.sh $i
    sed -i "" "s/#SBATCH --job-name/#SBATCH --job-name  ${i%/*}_${NM##*/}/g" $i"tryton.sh"
    sed -i "" "s/#SBATCH --output/#SBATCH --output    ${i%/*}_${NM##*/}/g" $i"tryton.sh"
    sed -i "" "s/#SBATCH --error/#SBATCH --error     ${i%/*}_${NM##*/}/g" $i"tryton.sh"
    sed -i "" "$ s/g16/g16  ${i%/*}_${NM##*/}.com > ${i%/*}_${NM##*/}.log/g" $i"tryton.sh"

  else
    echo tryton.sh file exists in $i directory.
  fi

done
