from msccls.figures.utils import \
  get_db, incremental_sum, run_successful, dump_vars
def get_data():
  db = get_db()
  runs = db.execute(f'SELECT * FROM test_run').fetchall()

  dates = {
    'total': {},
    'notCompleted': {},
    'successful': {},
  }

  for run in runs:
    date = run['t_start'].split(' ')[0]
    dates['total'].setdefault(date, 0)
    dates['total'][date] += 1
    if not run['t_stop'].strip():
      dates['notCompleted'].setdefault(date, 0)
      dates['notCompleted'][date] += 1
    if run_successful(run):
      dates['successful'].setdefault(date, 0)
      dates['successful'][date] += 1

  users = db.execute("SELECT * FROM test_user").fetchall()
  totalParticipants = len(users)
  totalTests = sum(dates['total'].values())
  totalTestsCorrect = sum(dates['successful'].values())
  totalTestsUncompleted = sum(dates['notCompleted'].values())
  ratioSuccess = (totalTestsCorrect-totalTestsUncompleted)/totalTests*100
  ratioSuccess = f"{ratioSuccess:.1f}"

  dump_vars([
    ('totalParticipants', totalParticipants),
    ('totalTests', totalTests),
    ('totalTestsCorrect', totalTestsCorrect),
    ('totalTestsUncompleted', totalTestsUncompleted),
    ('totalTestsIncorrect', totalTests-totalTestsUncompleted-totalTestsCorrect),
    ('varTotalRatioSuccess', ratioSuccess)
  ])


  return {
    'data': [incremental_sum(dates[k]) for k in ['total','successful']],
    'legend': ['Answers', 'Correct Answers'],
    'xlabel': "Date of test run",
    'ylabel': "Number of tests run",
  }
