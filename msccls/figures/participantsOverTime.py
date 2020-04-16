from msccls.figures.utils import get_db, incremental_sum
def get_data():
  db = get_db()
  runs = db.execute('SELECT t_created, str_id FROM test_user').fetchall()
  answers = db.execute("SELECT * FROM answer").fetchall()
  db.close()
  dates = {}

  answers_per_question = {}
  for answer in answers:
    answers_per_question.setdefault(answer['question'], []).append(answer)

  questions = [
    q for q in answers_per_question.keys() if q[:4] in ['init','inti']
  ]

  q_transform = {
    q:q.split('_', 1)[-1] for q in questions
  }
  q_final = {
    'age': 'age',
    'identifies': 'identifies as',
    'screen_size': 'screen size',
    'device_type': 'input type',
  }

  categories = {
    'identifies': ['female','male','other'],
    'device_type': ['mouse','trackpad','touch','other'],
    'screen': ['desktop','laptop','tablet','mobile'],
  }

  ans_data_per_q = {}
  for q,aans in answers_per_question.items():
    if q not in questions:
      continue
    q = q_final[q_transform[q]]
    for aa in aans:
      a = aa['answer']
      ans_data_per_q.setdefault(q, set())
      ans_data_per_q[q].add(aa['str_id'])

  completed_preq = ans_data_per_q['age']
  completed_post = ans_data_per_q['age']

  questions_post = [
    q for q in answers_per_question.keys() if q[:4] not in ['init','inti']
  ]
  questions_post = questions_post[5]
  completed_post = {a['str_id'] for a in answers_per_question[questions_post]}
  dates_preq = {}
  dates_post = {}

  for time, id_user in runs:
    date = time.split(' ')[0]
    dates.setdefault(date, 0)
    dates[date] += 1
    if id_user in completed_preq:
      dates_preq.setdefault(date, 0)
      dates_preq[date] += 1
    if id_user in completed_post:
      dates_post.setdefault(date, 0)
      dates_post[date] += 1

  return {
    'data': [incremental_sum(d) for d in [dates, dates_preq, dates_post]],
    'legend': [
      'Past consent form',
      'Completed pre-survey',
      'Completed post-survey'
    ],
    'xlabel': "Date of test-run",
    'ylabel': "Number of test-runs",
    'title': "Number of users at each milestone",
  }

if __name__ == "__main__":
  print(get_data())
