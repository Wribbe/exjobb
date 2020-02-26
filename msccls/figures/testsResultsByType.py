from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful

def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  tests_per_user = {}
  for run in testruns:
    user = run['id_user']
    tests_per_user.setdefault(user, []).append(run)

#  tests_per_user = dict([
#    (u,n) for u,n in tests_per_user.items() if len(n) < 16
#  ])

  tests_per_state = {}
  tests_per_state_outliers = {}
  for user, runs in tests_per_user.items():
    for run in runs:
      if len(runs) > 15:
        dic = tests_per_state_outliers
      else:
        dic = tests_per_state
      name = run['name']
      dic.setdefault(name, {})
      success = run_successful(run)
      dic[name].setdefault(success, 0)
      dic[name][success] += 1


  order = [
    'employee hours',
    'team workload',
    'task dependencies',
    'team performance'
  ]

  dh = 0.9/2

  ys_true, ys_false = [], []
  ys_true_outliers, ys_false_outliers = [], []
  init = 1.0*(len(order)-1)
  for i, name in enumerate(order):
    i = init-i
    total = sum([v for v in tests_per_state[name].values()])
    ys_true.append((i, tests_per_state[name][True]/total*100))
#    ys_false.append((i-dh*2-0.3, tests_per_state[name][False]/total*100))
    total = sum([v for v in tests_per_state_outliers[name].values()])
    ys_true_outliers.append((i-dh, tests_per_state_outliers[name][True]/total*100))
#    ys_false_outliers.append((i-dh*3-0.3, tests_per_state_outliers[name][False]/total*100))

  method = 'barh'

  data = [
    (zip(*ys_true)),
    (zip(*ys_true_outliers)),
  ]
  print(data)

  return {
    'data': data,
    'method': method,
    'kwargs': {
      'barh': {
        'height': dh,
      },
      'legend': {
        'fontsize': 'x-small',
      },
    },
    'yticks': zip(*[(init-i+dh/2-0.9/2, l.title()) for i,l in enumerate(order)]),
    'legend': [
      '#$r\leq15$',
      '#$r\geq16$',
    ],
    'xticks': range(0,110)[::10],
    'xlabel': 'Percentage of answers that are correct',
    'ylabel': 'Task type',
  }
