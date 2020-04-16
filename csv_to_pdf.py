#!/usr/bin/env python
import sys
import importlib
import itertools
from pathlib import Path
import matplotlib.pyplot as plt

from msccls.figures.utils import iter_markers, figure_units

def main(name_module, path_out):

  path_out = Path(path_out)

  name_module = Path(name_module).name.split('.')[0]
  module = importlib.import_module(f'msccls.figures.{name_module}')
  try:
    d = module.get_data(path_out)
  except TypeError:
    d = module.get_data()
  if not d:
    return
  f = plt.figure()

  lines = []
  methods = d.get('method',['plot'])
  if not type(methods) == list:
    methods = [methods]

  kwargs = d.get('kwargs', {})
  widths = d.get('widths', [])
  colors = d.get('colors', [])
  markers_list = d.get('markers', [[]])
  if not type(markers_list[0]) == list:
    markers_list = [markers_list]
  data = d['data']
  if not type(data[0]) == list:
    data = [data]

  labels_list = d.get('labels', [[]])

  for method in methods:
    if markers_list:
      markers = markers_list.pop(0)
    if labels_list:
      labels = labels_list.pop(0)
    for (xs, ys), marker in zip(data.pop(0), iter_markers(method)):
      method_kwargs = kwargs.get(method, {})
      if method in ['barh', 'bar']:
        if widths:
          method_kwargs['width'] = widths.pop(0)
        if colors:
          method_kwargs['color'] = colors.pop(0)
        if markers:
          method_kwargs['hatch'] = markers.pop(0)
        else:
          method_kwargs['hatch'] = marker
        if not 'alpha' in method_kwargs:
          method_kwargs['alpha'] = 0.99
        if not 'edgecolor' in method_kwargs:
          method_kwargs['edgecolor'] = 'black'
        lines.append(getattr(plt, method)(xs, ys, **method_kwargs))
      elif method == 'scatter':
        lines.append(getattr(plt, method)(xs, ys, **method_kwargs))
      elif method == 'stackplot':
        lines.append(getattr(plt, method)(xs, *ys, **method_kwargs))
      else: # Default to a line plot.
        if markers:
          marker = markers.pop(0)
        if labels:
          method_kwargs['label'] = labels.pop(0)
        lines.append(plt.plot(xs, ys, marker, **method_kwargs))

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
    if not 'legend' in d and labels_list:
      plt.legend()


  f.set_size_inches(d.get('size', figure_units['size']))
  f.tight_layout()
  f.savefig(path_out, bbox_inches='tight')

if __name__ == "__main__":
  main(*sys.argv[1:])
