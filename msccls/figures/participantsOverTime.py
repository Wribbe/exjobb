from msccls.figures.utils import get_db, incremental_sum
def get_data():
  db = get_db()
  runs = db.execute('SELECT t_created, str_id FROM test_user').fetchall()
  dates = {}
  for time, id_user in runs:
    date = time.split(' ')[0]
    dates.setdefault(date, 0)
    dates[date] += 1
  return {
    'data': [incremental_sum(dates)],
    'xlabel': 'Date of registration',
    'ylabel': 'Number of participants',
    'title': 'Total amount of participants over time',
  }
