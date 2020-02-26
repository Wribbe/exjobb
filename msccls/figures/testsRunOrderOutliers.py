from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors

import matplotlib as plt
import numpy as np

def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  tests_per_user = {}
  for run in testruns:
    user = run['id_user']
    tests_per_user.setdefault(user, []).append(run['name'])

  tests_per_user = [(u,n) for u,n in tests_per_user.items() if len(n) > 15]
  types = {}
  data, widths, xticks, xlabels, colors, markers = [], [], [], [], [], []

  group_width = 0.8

  for _, names in tests_per_user:
    for x, name in enumerate(names, start=1):
      types.setdefault(x, {})
      types[x].setdefault(name, 0)
      types[x][name] += 1

  order = [
    'employee hours',
    'team workload',
    'task dependencies',
    'team performance'
  ]

  method = 'bar'
  mappings_style = dict(zip(order, zip(iter_colors, iter_markers(method))))
  handlers_for_legend = {n: 0 for n in order}

  bar_num = 0
  for x, dict_types in types.items():
    total = sum(dict_types.values())
    sum_prev = 0
    bars_at_x = []
    for name, value in sorted(dict_types.items(), key=lambda x:-x[1]):
      value = value/total*100
      bars_at_x.append((name, value+sum_prev))
      sum_prev += value

    # Print in inverted order.
    for name, value in reversed(bars_at_x):
      if value == 0:
        continue
      handlers_for_legend[name] = bar_num
      color, marking = mappings_style[name]
      colors.append(color)
      markers.append(marking)
      bar_num += 1
      data.append((x, value))

  return {
    'data': data,
    'method': method,
    'legend': handlers_for_legend,
    'markers': markers,
    'colors': colors,
    'yticks': range(110)[::10],
    'xticks': [1] + list(range(10, 110)[::10]),
    'ylabel': "Task-type percentages",
    'xlabel': "Test index, from the first test-run and onwards",
    'kwargs': {
      'legend': {
        'bbox_to_anchor': (1.0, 0.5),
        'loc': 'center right',
        'fontsize': 'small',
      },
      'bar': {
        'linewidth': 1,
      }
    }
  }
