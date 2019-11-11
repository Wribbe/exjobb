#!/bin/sh
DIR_OUT="mockups"
if [ "$1" = "--single" ]; then
    wget -qO- http://localhost:8000/mockup/$2/$3 | inkscape -A "mockup.pdf" -
else
  for b in 1; do
    [ -d ${DIR_OUT}/$b ] || mkdir -p ${DIR_OUT}/$b
    for i in 1 2 3 4; do
      wget -qO- --no-proxy http://localhost:8000/mockup/$b/$i | inkscape -A "${DIR_OUT}/$b/mockup_$i.pdf" -
    done
    qpdf --empty --pages ${DIR_OUT}/$b/*.pdf -- mockups_batch_$b.pdf
  done
fi
