
from msccls.figures.utils import *
from msccls.figures.utils import fix
from scipy.stats import norm

import matplotlib.pyplot as plt
import numpy as np


def get_data(path_out):

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()
  testruns = fix.testruns(testruns)

  dx = 0.9/4

  labels = order
  handler = {}
  colors = []
  markers = []
#  mappings_style = dict(zip(order, zip(iter_colors, iter_markers('bar'))))
  num_bar = 0

  def data_get(valid):
    tests_per_user = {}
    for run in testruns:
      user = run['id_user']
      tests_per_user.setdefault(user, 0)
      tests_per_user[user] += 1

    valid_users = [u for u,num in tests_per_user.items() if valid(num)]

    run_per_diff = {}
    for run in testruns:
      if not run['id_user'] in valid_users:
        continue
      start, stop = run_to_datetimes(run)
      diff = (stop-start)
      diff = round(diff.seconds + diff.microseconds/1e6)
      run_per_diff.setdefault(diff, 0)
      run_per_diff[diff] += 1

    data = []
    largest = (0,0)
    for diff, num_runs in run_per_diff.items():
      if largest[1] <= num_runs:
        largest = (diff, num_runs)
      data.append((diff, num_runs))
    return data, largest

  runs_per_type = {}
  for run in testruns:
    test_type = run['name']
    start, stop = run_to_datetimes(run)
    diff = (stop-start)
    diff = round(diff.seconds + diff.microseconds/1e6)
    runs_per_type.setdefault(test_type, {})
    runs_per_type[test_type].setdefault(diff, 0)
    runs_per_type[test_type][diff] += 1

  list_data = [data_get(valid=l) for l in [
#    lambda num: True,
    lambda num: num<16,
    lambda num: num>15,
  ]]

  largest = list_data[0][1]
#  data = [(zip(*data)) for data, _ in list_data]
#  for x, type_run in enumerate(labels):
#    most = (0,0)
#    loc_data = runs_per_type[type_run]
#    handler[type_run] = -4+x
#    for x,num in loc_data.items():
#      if num > most[1]:
#        most = (x,num)
#    data.append([most])


#  data = [data] + [
#    [
#      ([x+i for x in range(10,20)], list(range(10,20)))
#    ] for i in list(range(40))[::10]
#  ]

  fig, axs = plt.subplots(len(list_data), 1, sharex=True)
  fig.subplots_adjust(hspace=0)

  handlers = []
  list_data = list(zip(list_data, iter_colors, iter_markers('bar')))
  xticks = [1]+list(range(10, 150)[::10])
  lines_90 = []
  lines_50 = []
  for i, ((d, largest), color, hatch) in enumerate(list_data):
    axs[i].set_ylim(top=100)
    line_90 = 0
    line_50 = 0
    sum_y = 0
    xs, ys = zip(*d)
    total_y = sum(ys)
    for x,y in sorted(d):
      sum_y += y
      if sum_y/total_y >= 0.9 and not line_90:
        line_90 = x+1
        lines_90.append(line_90)
      if sum_y/total_y >= 0.5 and not line_50:
        line_50 = x+1
        lines_50.append(line_50)
    handlers.append(axs[i].bar(
      xs, ys,
      color=color,
      hatch=hatch,
      alpha=0.99,
      edgecolor='black'
    ))
    yticks = []
    for tick in list(range(0, 120)[::20])[1:]:
      diff = abs(largest[1]-tick)
      if diff < 10:
        yticks.append(largest[1])
      else:
        yticks.append(tick)

    axs[i].set_yticks(yticks)
  h90 = ""
  h50 = ""
  for i, line in enumerate(lines_90):
    ys = range(0,120)[::20]
    h90 = axs[i].plot([line]*len(ys), ys, "--", zorder=-10, alpha=0.8,
                  linewidth=1)[0]
  for i, line in enumerate(lines_50):
    ys = range(0,120)[::20]
    h50 = axs[i].plot([line]*len(ys), ys, "-.", zorder=-10, alpha=0.8,
                  linewidth=1)[0]
  fig.legend(
    [
      *handlers,
      h90,
      h50,
    ],
    [
#      'All users',
      '#$r\leq15$',
      '#$r\geq16$',
      '90th percentile',
      '50th percentile',
    ],
    loc='upper right',
    bbox_to_anchor=(0.88, 1.00),
    fontsize='small',
  )
  for i in range(len(list_data)):
    axs[i].vlines(xticks, 0, 100, alpha=0.2, linestyles='dotted', linewidth=1,
                  zorder=-20)
    axs[i].vlines([v+5 for v in xticks[:-1]], 0, 100, alpha=0.1,
                  linestyles='dotted', linewidth=1, zorder=-20)
  fig.set_size_inches(figure_units['size'])
  plt.xticks(xticks)
  fig.add_subplot(111, frameon=False)
  plt.tick_params(labelcolor='none', top=False, bottom=False, right=False,
                  left=False)
  plt.title('Histogram for all completion times, regular and outlier')
  plt.xlabel('Seconds')
  plt.ylabel('Size of group')
  #fig.tight_layout()
  figure_save(fig, path_out)

  return None
#  return {
##    'method': ['bar'] + ['plot']*4,
#    'method': 'bar',
##    'markers': [[], ['X'],['d'],['P'],['v']],
#    'data': data,
#    'xticks': list(range(0, 140)[10::10]) + [largest[0]],
#    'yticks': list(range(0, 90)[::10]) + [largest[1]],
##    'yticks': ([x-0.9/4 for x in range(len(labels))], [l.title() for l in labels]),
##    'labels': [[], ['A'],['B'],['C'],['D']],
##    'legend': handler,
#    'legend': ['Total'],
#    'ylabel': "Number of runs",
#    'xlabel': "Seconds",
#    'kwargs': {
#      'legend': {
#        'fontsize': 'small',
#      },
#  #    'bar': {
#  #      'alpha': 0.33,
#  #    },
#    }
#  }
#

