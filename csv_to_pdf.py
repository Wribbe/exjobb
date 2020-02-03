#!/usr/bin/env python
import os
import sys

from pathlib import Path
import matplotlib.pyplot as plt

def main(path_data, path_out):
  path_data, path_out = [Path(p) for p in [path_data, path_out]]
  data = path_data.read_text().splitlines()
  code, header, *data = data
  code = os.linesep.join([l for l in code.split(';') if l.strip()])
  datasets = []
  exec(code)
  f = plt.figure()
  for (x, y) in datasets:
    plt.plot(x, y, "o-")
  f.set_size_inches(5, 3)
  f.savefig(path_out, bbox_inches='tight')

if __name__ == "__main__":
  main(*sys.argv[1:])
