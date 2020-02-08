from msccls.figures.utils import get_db, dump_vars, as_percent
def get_data():
  db = get_db()
  testruns = db.execute("SELECT * FROM test_run").fetchall()
  test_types = {}
  for run in testruns:
    name = run['name']
    test_types.setdefault(name, 0)
    test_types[name] += 1

  test_types = {
    k:v for k,v in sorted(test_types.items(), key=lambda x: x[1])
  }

  xs = [t.title() for t in test_types.keys()]
  ys = list(test_types.values())

  db.close()

  return {
    'data': [(xs, ys)],
    'method': 'barh',
#    'xticks': [0,50,100, 150,]
    'ylabel': "Task type",
    'xlabel': "Number of test run",
  }
