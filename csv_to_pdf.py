#!/usr/bin/env python
import os
import sys

from pathlib import Path
import matplotlib.pyplot as plt

def main(path_data, path_out):
  path_data, path_out = [Path(p) for p in [path_data, path_out]]
  data = path_data.read_text().splitlines()
  code, header, title, xlabel, ylabel, legend, *data = data
  code = os.linesep.join([l for l in code.split(';') if l.strip()])
  datasets = []
  exec(code)
  f = plt.figure()
  lines = []
  markers = ['o-', 'v--']
  for (x, y), marker in zip(datasets, markers):
    lines.append(plt.plot(x, y, marker))
  f.set_size_inches(6, 3)
  if legend:
    plt.legend([l[0] for l in lines], legend.split(','))
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.title(title)

  f.savefig(path_out, bbox_inches='tight')

if __name__ == "__main__":
  main(*sys.argv[1:])
