from msccls.figures.utils import \
  get_db, dump_vars, as_percent, iter_markers, iter_colors, run_successful, \
  fix


def get_data():

  db = get_db()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  testruns = fix.testruns(testruns)
  db.close()

  data = [
    (range(10), range(10)),
  ]


  return {
    'data': data,
  }


