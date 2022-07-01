#!/bin/bash

DIR=$(ls -d */)

for i in $DIR; do
  if [[ ! -f "$i/tryton.sh" ]]; then
    echo $i"tryton.sh" is writting:
    cp tryton.sh $i
    sed -i "" "s/ARG/${i%/*}/g" $i"tryton.sh"
  else
    echo tryton.sh file exists in $i directory.
  fi

done
