#!/bin/bash

mkdir -p './artifacts/functions'
mkdir -p './artifacts/layers'


## create zip with code
for d in ./services/* ; do
  if [ ! -d "$d" ]; then
    continue
  fi

  for f in $d/functions/* ; do
    if [ ! -d "$f" ]; then
      continue
    fi

    zip_name="${d##*/}-service_${f##*/}"

    for file in $f/* ; do
      if (grep -l 'test' $file) then
        echo "Not insert " $file "in zip"
      else
        zip -rj ./artifacts/functions/$zip_name.zip $file
      fi

    done


    printf '@ main.py\n@=lambda_function.py\n' | zipnote -w ./artifacts/functions/$zip_name.zip
  done
done