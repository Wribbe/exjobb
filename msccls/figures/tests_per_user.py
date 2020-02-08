from msccls.figures.utils import get_db, dump_vars, as_percent
def get_data():
  db = get_db()
  testruns = db.execute("SELECT * FROM test_run").fetchall()
  users = db.execute("SELECT * FROM test_user").fetchall()
  db.close()
  runs_per_user = {}
  for run in testruns:
    id_user = run['id_user']
    runs_per_user.setdefault(id_user, 0)
    runs_per_user[id_user] += 1

  number_of_runs = {}
  for user, val in sorted(runs_per_user.items(), key=lambda t: t[1]):
    number_of_runs.setdefault(val, 0)
    number_of_runs[val] += 1

  val_num_any_tests_run = sum(number_of_runs.values())
  val_tests_five_to_ten = 0
  val_tests_eleven_or_more = 0
  num_users = len(users)
  val_test_no_tests = num_users - val_num_any_tests_run
  for num_runs, num_users in number_of_runs.items():
    if 5 >= num_runs <= 9:
      val_tests_five_to_ten += num_users
    elif num_runs > 9:
      val_tests_eleven_or_more += num_users

#  val_num_any_tests_run_p = val_num_any_tests_run/num_users
#  val_num_five_or_more_test_run_p = val_num_five_or_more_test_run/num_users

  # Convert to latex formatted percentages.
#  val_num_any_tests_run_p = as_percent(val_num_any_tests_run_p)
#  val_num_five_or_more_test_run_p = as_percent(val_num_five_or_more_test_run_p)

  dump_vars([
    ('val_num_any_tests_run', val_num_any_tests_run),
    ('val_tests_five_to_ten', val_tests_five_to_ten),
    ('val_tests_eleven_or_more', val_tests_eleven_or_more),
    ('val_test_no_tests', val_test_no_tests),
#    ('val_num_any_tests_run_p', val_num_any_tests_run_p),
  ])

  x = list(number_of_runs.keys())
  y = list(number_of_runs.values())
  return {
    'data': [(x,y)],
    'method': 'bar',
    'xticks': [1,5,10]+list(number_of_runs.keys())[-3:],
    'yticks': list(set(number_of_runs.values()))[-3:],
    'xlabel': "Number of test run",
    'ylabel': "Number of users in category",
#    'table': {
#      'cellText': [(f"{x}:", y) for x,y in zip(x,y)],
#      'colLabels': ['Tests Run','#Users'],
#      'loc': 'upper right',
#      'colWidths': [0.15, 0.15],
#      'cellLoc': 'center',
#      'bbox': [0, -0.3, 1, 0.275],
#    },
#    'table_cell_height': 0.07,
  }
