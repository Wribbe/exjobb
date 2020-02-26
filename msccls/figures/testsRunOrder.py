from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors

def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  tests_per_user = {}
  for run in testruns:
    user = run['id_user']
    tests_per_user.setdefault(user, []).append(run['name'])

  tests_per_user = [(u,n) for u,n in tests_per_user.items() if len(n) < 16]
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

  method = "bar"
  mappings_style = dict(zip(order, zip(iter_colors, iter_markers(method))))
  handlers_for_legend = {}
  num_bar = 0
  for x, dict_types in types.items():
    xticks.append(x+group_width/2)
    xlabels.append(x)
    total = sum(dict_types.values())
    i = 0
    for name in order:
      value = dict_types.get(name)
      if not value:
        continue
      widths.append(group_width/len(dict_types))
      color, marker = mappings_style[name]
      colors.append(color)
      markers.append(marker)
      handlers_for_legend[name] = num_bar
      dx = widths[-1]
      bx = x+dx/2+dx*i
      by = (value/total*100)
      data.append((bx, by))
      num_bar += 1
      i += 1

  return {
    'data': data,
    'method': method,
    'xticks': (xticks, xlabels),
    'yticks': range(110)[::10],
    'widths': widths,
    'markers': markers,
    'colors': colors,
    'legend': handlers_for_legend,
    'kwargs': {
      'legend': {
        'fontsize': 'x-small',
        'loc': 'upper left',
        'bbox_to_anchor': [.22, 1.0],
      },
    },
   'ylabel': "Task percentage",
   'xlabel': "Test index, from the first test-run and onwards",
  }
