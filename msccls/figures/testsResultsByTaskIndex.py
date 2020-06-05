from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful

def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  tests_per_user = {}
  for run in testruns:
    id_user = run['id_user']
    tests_per_user.setdefault(id_user, []).append(run)

  success_per_type = {'regular': {}, 'outlier': {}}
  for _, runs in tests_per_user.items():
    if len(runs) > 15:
      dic = success_per_type['outlier']
    else:
      dic = success_per_type['regular']
    for x, run in enumerate(runs, start=1):
      if x > 15:
        break
#      run_type = run['name']
#      dic.setdefault(run_type, {})
      dic.setdefault(x, {})
      result = run_successful(run)
      dic[x].setdefault(result, 0)
      dic[x][result] += 1

  data = {'regular': [], 'outlier': []}
  for type_result, x_dics in success_per_type.items():
    for _, values in x_dics.items():
      total = sum(values.values())
      val = values.get(True, 0)
      data[type_result].append(val/total*100)

  dx = 0.9/2

  data = [
    (zip(*[(i-dx/2, v) for i,v in enumerate(data['regular'], start=1)])),
    (zip(*[(i+dx/2, v) for i,v in enumerate(data['outlier'], start=1)])),
  ]

  method = 'bar'

  return {
    'data': data,
    'method': method,
    'xticks': range(1,16),
    'yticks': range(110)[::10],
#    'widths': 0.9/2,
#    'markers': markers,
#    'colors': colors,
#    'legend': handlers_for_legend,
    'kwargs': {
      'legend': {
        'fontsize': 'x-small',
#        'loc': 'upper left',
#        'bbox_to_anchor': [.22, 1.0],
      },
      'bar': {
        'width': dx,
      }
    },
   'ylabel': "Percentage",
   'xlabel': "Test index, from the first test-run and onwards",
  }
