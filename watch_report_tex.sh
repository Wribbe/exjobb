#!/bin/sh
path_dir="msccls"

inotifywait -m --timefmt '%d/%m/%y %H:%M' --format '%e %T %w %f' \
-e modify ${path_dir} | while read event date time dir file; do
  if [ "${file}" == "report.tex" ]; then
    make
    echo "At ${time} on ${date}, was ${file} recompiled."
  fi
done
