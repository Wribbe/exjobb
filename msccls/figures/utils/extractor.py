#!/usr/bin/env python

import re

from datetime import datetime, timedelta
from pathlib import Path

def get():

  path_data = Path(Path(__file__).parent.resolve(), 'data.txt')
  data = [l.strip() for l in path_data.read_text().splitlines()]
  ips = {}
  ret = {}
  for line in data:
    if not 'exjobb/webapp' in line:
      continue
    if 'abort' in line:
      continue
    if not 'GET' in line and not 'POST' in line:
      continue
    if '/favicon.ico' in line:
      continue
  #  line = line.split('- ', 2)[-1]
  #  if '?fbclid' in line:
  #    line = re.sub(r'\?fbclid=\S*', '', line)
    date = line.split('[')[-1].split(']')[0]
    date = datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')
    # Shift to utc and remove tzinfo.
    date -= timedelta(hours=1)
    date = date.replace(tzinfo=None)

    #if not 'POST' in line:
    #  continue
    #print(line)
#    key = "GET" if "GET" in line else "POST"
    ret.setdefault(date, []).append(line)

  return ret

if __name__ == "__main__":
  print(get())
