from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful

def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  tests_per_user = {}
  user_totals = {}
  for run in testruns:
    id_user = run['id_user']
    tests_per_user.setdefault(id_user, {})
    type_run = run['name']
    tests_per_user[id_user].setdefault(type_run, []).append(run)
    user_totals.setdefault(id_user, 0)
    user_totals[id_user] += 1

  for user, value in user_totals.items():
    if value < 16:
      del tests_per_user[user]

  results_per_type = {}
  for user, dict_types in tests_per_user.items():
    for run_type, runs in dict_types.items():
      results_per_type.setdefault(run_type, [])
      data_run_user = []
      result_history = []
      for x, run in enumerate(runs, start=1):
        success = run_successful(run)
        result_history.append(success)
        prob = len([v for v in result_history if v])/len(result_history)*100
        data_run_user.append((x, prob))
      results_per_type[run_type].append(data_run_user)


  order = [
    'employee hours',
    'team workload',
    'task dependencies',
    'team performance',
  ]

  data = []
  for name in order:
    data_lists = results_per_type[name]
    for run_user in data_lists:
      data.append((zip(*run_user)))

  dx = 0.9/2

  return {
    'data': data,
#    'legend': [l.title() for l in order],
    'method': 'lines',
#    'xticks': range(1,16),
#    'yticks': range(110)[::10],
#    'widths': 0.9/2,
#    'markers': markers,
#    'colors': colors,
#    'legend': handlers_for_legend,
#    'kwargs': {
#      'legend': {
#        'fontsize': 'x-small',
##        'loc': 'upper left',
##        'bbox_to_anchor': [.22, 1.0],
#      },
#      'scatter': {
#        'alpha': 0.7,
#        's': 2,
#      }
#    },
   'ylabel': "Task percentage",
   'xlabel': "Test index, from the first test-run and onwards",
  }
