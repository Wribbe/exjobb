#!/usr/bin/env python
import sys
import importlib

from pathlib import Path
import matplotlib.pyplot as plt

def main(name_module, path_out):

  path_out = Path(path_out)

  name_module = Path(name_module).name.split('.')[0]
  module = importlib.import_module(f'msccls.figures.{name_module}')
  d = module.get_data()
  f = plt.figure()

  lines = []
  markers = ['o-', 'v--',]
  method = d.get('method','plot')
  for (xs, ys), marker in zip(d['data'], markers):
    if method in ['barh', 'bar']:
      lines.append(getattr(plt, method)(xs, ys))
    else: # Default to a line plot.
      lines.append(plt.plot(xs, ys, marker))

  if 'legend' in d:
    plt.legend([l[0] for l in lines], d['legend'])
  if 'xlabel' in d:
    plt.xlabel(d['xlabel'])
  if 'ylabel' in d:
    plt.ylabel(d['ylabel'])
  if 'title' in d:
    plt.title(d['title'])
  if 'xticks' in d:
    plt.xticks(d['xticks'])
  if 'yticks' in d:
    plt.yticks(d['yticks'])
  if 'table' in d:
    table = plt.table(**d['table'])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
  if 'table_cell_height' in d:
    for cell in table.properties()['child_artists']:
      print(cell._text.get_position())
      cell.set_height(d['table_cell_height'])
    for cell in table.properties()['child_artists'][::2]:
      pass


  f.set_size_inches(d.get('size', (6, 3)))
  f.tight_layout()
  f.savefig(path_out, bbox_inches='tight')

if __name__ == "__main__":
  main(*sys.argv[1:])
