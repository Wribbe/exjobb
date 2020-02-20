#!/usr/bin/env python
import sys
import importlib
import itertools
from pathlib import Path
import matplotlib.pyplot as plt

from msccls.figures.utils import iter_markers

def main(name_module, path_out):

  path_out = Path(path_out)

  name_module = Path(name_module).name.split('.')[0]
  module = importlib.import_module(f'msccls.figures.{name_module}')
  d = module.get_data()
  f = plt.figure()

  lines = []
  method = d.get('method','plot')

  kwargs = d.get('kwargs', {})
  widths = d.get('widths', [])
  colors = d.get('colors', [])
  markers = d.get('markers', [])

  for (xs, ys), marker in zip(d['data'], iter_markers(method)):
    method_kwargs = kwargs.get(method, {})
    if method in ['barh', 'bar']:
      if widths:
        method_kwargs['width'] = widths.pop(0)
      if colors:
        method_kwargs['color'] = colors.pop(0)
      if markers:
        method_kwargs['marker'] = markers.pop(0)
      lines.append(
        getattr(plt, method)(
          xs, ys, hatch=marker, alpha=.99, edgecolor='black', **method_kwargs
        )
      )
    elif method == 'scatter':
      lines.append(getattr(plt, method)(xs, ys, **method_kwargs))
    elif method == 'stackplot':
      lines.append(getattr(plt, method)(xs, *ys, **method_kwargs))
    else: # Default to a line plot.
      lines.append(plt.plot(xs, ys, marker))

  if 'legend' in d:
    if type(d['legend']) == dict:
      labels = [l.title() for l in d['legend'].keys()]
      handlers = [lines[d['legend'][l.lower()]] for l in labels]
      plt.legend(handlers, labels, **kwargs.get('legend', {}))
    elif method == 'stackplot':
      plt.legend(**kwargs.get('legend'))
    else:
      plt.legend([l[0] for l in lines], d['legend'], **kwargs.get('legend', {}))
  if 'xlabel' in d:
    plt.xlabel(d['xlabel'])
  if 'ylabel' in d:
    plt.ylabel(d['ylabel'])
  if 'title' in d:
    plt.title(d['title'])
  if 'xticks' in d:
    try:
      plt.xticks(*d['xticks'])
    except TypeError:
      plt.xticks(d['xticks'])
  if 'yticks' in d:
    try:
      plt.yticks(*d['yticks'])
    except TypeError:
      plt.yticks(d['yticks'])
  if 'table' in d:
    table = plt.table(**d['table'])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
  if 'table_cell_height' in d:
    for cell in table.properties()['child_artists']:
      cell.set_height(d['table_cell_height'])
    for cell in table.properties()['child_artists'][::2]:
      pass


  f.set_size_inches(d.get('size', (6, 3)))
  f.tight_layout()
  f.savefig(path_out, bbox_inches='tight')

if __name__ == "__main__":
  main(*sys.argv[1:])
