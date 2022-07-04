#!/bin/bash

c=0
ARR=() # Tablica do ktorej dodawane sa nazwy zadan z wszystkich dostepnych skryptow tryton.sh
DIR=$(ls -d */)
SQU=$(squeue --format="%j" --me) # lista aktualnie prowadzonych zadan

for i in $DIR; do
	c=$((c+1))
	z=$(sed "2q;d" $i"tryton.sh")
	ARR[c]=${z#*--job-name}
done

# Sprawdzanie czy nazwa skryptu z tryton.sh nie jest wykonywana w sbatch 
for i in ${ARR[@]}; do
	if [[ ! $SQU == *$i* ]]; then
		for j in $DIR; do
			j=${j%/*}
			if [[ $i == *$j* ]]; then
				echo running: $j/tryton.sh
				sbatch $j/tryton.sh
			fi
		done
	fi
done

