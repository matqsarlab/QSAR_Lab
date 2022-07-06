#!/bin/bash

for i in $@; do
  T=$(tail $i)

  if [[ "$T" == *Error* ]]; then
    echo $i
  fi
done
