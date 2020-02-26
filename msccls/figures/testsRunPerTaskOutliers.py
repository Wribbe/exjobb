from msccls.figures.utils import get_db, dump_vars, as_percent
def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run").fetchall()
  db.close()

  tests_per_user = {}
  for run in testruns:
    name = run['name']
    user = run['id_user']
    tests_per_user.setdefault(user, {})
    tests_per_user[user].setdefault(name, 0)
    tests_per_user[user][name] += 1

  labels = list(list(tests_per_user.values())[0].keys())
  dicts = [d for d in tests_per_user.values() if sum(d.values()) > 15]
  dicts = sorted(dicts, key=lambda d: -sum(d.values()))
  # Remove the last two r = 20 from list, same distribution.
  dicts = dicts[:-2]
  height = 0.9/len(dicts)

  data = []
  for i, dic in enumerate(dicts):
    ys = [dic[l] for l in labels]
    data.append(([height*-i-ii for ii,_ in enumerate(ys)], ys))

  return {
    'data': data,
    'method': 'barh',
    'yticks': [-x+height/2-0.9/2 for x in range(len(labels))],
    'ylabel': "Task type",
    'xlabel': "Total number of tests",
    'xticks': range(0,40)[::5],
    'legend': [f'#$r={sum(d.values())}$' for d in dicts],
    'kwargs': {
      'legend': {
        'title': "Runs/User:",
        'fontsize': "x-small",
      },
      'barh': {
        'height': height,
        'tick_label': [l.title() for l in labels],
      }
    }
  }
