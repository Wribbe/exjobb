from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful, \
  fix, order, run_to_datetimes


def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()
  testruns = fix.testruns(testruns)

  dx = 0.9/2

  labels = list(reversed(order))

  tests_per_user = {}
  for run in testruns:
    user = run['id_user']
    tests_per_user.setdefault(user, 0)
    tests_per_user[user] += 1

  valid_users = [u for u,num in tests_per_user.items() if num < 16]

  run_per_type = {}
  for run in testruns:
    if not run['id_user'] in valid_users:
      continue
    test_type = run['name']
    start, stop = run_to_datetimes(run)
    diff = stop-start
    run_per_type.setdefault(test_type, []).append(diff)


  data = []
  for x, l in enumerate(labels):
    times = sorted(run_per_type[l])
    len_times = len(times)
    average = sum([d.seconds for d in times])/len_times
    if len_times-1%2:
      mean = times[int((len_times-1)/2)].seconds
    else:
      index = int((len_times-1)/2)
      mean = (times[index] + times[index+1]).seconds/2
    data.append((x+dx/2, average))
    data.append((x-dx/2, mean))


  data = [
    (zip(*data[0::2])),
    (zip(*data[1::2])),
  ]


  return {
    'method': 'barh',
    'data': data,
    'yticks': (range(len(labels)), [l.title() for l in labels]),
    'legend': ['Average','Median'],
    'ylabel': "Task type",
    'xlabel': "Seconds",
    'kwargs': {
      'barh': {
        'height': dx,
      },
#      'legend': {
#        'fontsize': 'x-small',
#      }
    }
  }


