from msccls.figures.utils import get_db, dump_vars, as_percent
def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run").fetchall()
  db.close()

  test_types = {}
  tests_per_user = {}
  for run in testruns:
    name = run['name']
    test_types.setdefault(name, 0)
    test_types[name] += 1

    user = run['id_user']
    tests_per_user.setdefault(user, []).append(run)

  test_types = {
    k:v for k,v in sorted(test_types.items(), key=lambda x: -x[1])
  }

  tests_ten_and_below = {}
  tests_above_ten = {}
  for user, runs in tests_per_user.items():
    if len(runs) > 15:
      dic = tests_above_ten
    else:
      dic = tests_ten_and_below
    for run in runs:
      name = run['name']
      dic.setdefault(name, 0)
      dic[name] += 1

  labels = list(test_types.keys())
  dics = [test_types, tests_ten_and_below, tests_above_ten]
  height = 0.9/len(dics)

  data = []
  for i, dic in enumerate(dics):
    ys = [dic[l] for l in labels]
    data.append(([height*-i-ii for ii,_ in enumerate(ys)], ys))

  return {
    'data': data,
    'method': 'barh',
    'yticks': [-x-height/2 for x in range(len(labels))],
    'ylabel': "Task type",
    'xlabel': "Number of test-runs",
    'legend': ['#$r>0$', '#$r\leq15$', '#$r\geq16$'],
    'title': 'Test-runs grouped by test type',
    'kwargs': {
      'legend': {
        'title': "Runs/User:",
      },
      'barh': {
        'height': height,
        'tick_label': [l.title() for l in labels],
      }
    }
  }
