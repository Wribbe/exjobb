from msccls.figures.utils import \
  get_db, incremental_sum, run_successful, dump_vars
def get_data():
  db = get_db()
  runs = db.execute(f'SELECT * FROM test_run').fetchall()

  dates = {
    'total': {},
    'not_completed': {},
    'successful': {},
  }

  for run in runs:
    date = run['t_start'].split(' ')[0]
    dates['total'].setdefault(date, 0)
    dates['total'][date] += 1
    if not run['t_stop'].strip():
      dates['not_completed'].setdefault(date, 0)
      dates['not_completed'][date] += 1
    if run_successful(run):
      dates['successful'].setdefault(date, 0)
      dates['successful'][date] += 1

  users = db.execute("SELECT * FROM test_user").fetchall()
  total_participants = len(users)
  total_tests = sum(dates['total'].values())
  total_tests_correct = sum(dates['successful'].values())
  total_tests_uncompleted = sum(dates['not_completed'].values())
  ratio_success = (total_tests_correct-total_tests_uncompleted)/total_tests*100
  ratio_success = f"{ratio_success:.1f}"

  dump_vars([
    ('total_participants', total_participants),
    ('total_tests', total_tests),
    ('total_tests_correct', total_tests_correct),
    ('total_tests_uncompleted', total_tests_uncompleted),
    ('total_tests_incorrect', total_tests-total_tests_uncompleted-total_tests_correct),
    ('var_total_ratio_success', ratio_success)
  ])


  return {
    'data': [incremental_sum(dates[k]) for k in ['total','successful']],
    'legend': ['Answers', 'Correct Answers'],
    'xlabel': "Date of test run",
    'ylabel': "Number of tests run",
  }
