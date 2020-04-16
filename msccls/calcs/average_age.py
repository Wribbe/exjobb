#!/usr/bin/env python

import subprocess
import sys


try:
  from msccls.figures.utils import *
  from msccls.figures.utils import fix
except ModuleNotFoundError as e:
  import os
  os.environ['PYTHONPATH'] = os.getcwd()
  subprocess.call(['python', __file__])
  sys.exit()

def get_data():

  db = get_db()
  users = db.execute("SELECT * FROM test_user").fetchall()
  answers = db.execute("SELECT * FROM answer").fetchall()
  testruns = db.execute("SELECT * FROM test_run WHERE t_stop").fetchall()
  db.close()

  testruns = fix.testruns(testruns)

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
    for a in aans:
      a = a['answer']
      ans_data_per_q.setdefault(q, {})
      ans_data_per_q[q].setdefault(a, 0)
      ans_data_per_q[q][a] += 1

  questions_post = [
    q for q in answers_per_question.keys() if q[:4] not in ['init','inti']
  ][5:][:-1]
  completed_post = {a['str_id'] for a in answers_per_question[questions_post[0]]}

  ans_data_per_q_post = {}
  for q,aans in answers_per_question.items():
    if q not in questions:
      continue
    q = q_final[q_transform[q]]
    for a in aans:
      if not a['str_id'] in completed_post:
        continue
      a = a['answer']
      ans_data_per_q_post.setdefault(q, {})
      ans_data_per_q_post[q].setdefault(a, 0)
      ans_data_per_q_post[q][a] += 1


  for d in [ans_data_per_q, ans_data_per_q_post]:
    sum_ages = 0
    sum_num = 0
    for age, num in d['age'].items():
      sum_num += int(num)
      sum_ages += int(age)*int(num)
    dataset = 'pre' if d == ans_data_per_q else 'post'
    print(f"Average age ({dataset}): {sum_ages}/{sum_num}: {sum_ages/sum_num}")

  for d in [ans_data_per_q, ans_data_per_q_post]:
    gen_total = sum(d['identifies as'].values())
    for ident, num in d['identifies as'].items():
      percent = num/gen_total*100
      dataset = 'pre' if d == ans_data_per_q else 'post'
      print(f"Identifies as ({dataset}): {ident}: {num}/{gen_total} ({percent})")

  last_runs = {}
  for run in testruns:
    user  = run['id_user']
    if not user in completed_post:
      continue
    t_stop = run['t_stop']
    t_stop = datetime.strptime(t_stop,'%Y-%m-%d %H:%M:%S.%f%Z')
    if not last_runs.get(user):
      last_runs[user] = t_stop
    if t_stop > last_runs[user]:
      last_runs[user] = t_stop

  users = {u['str_id']: u for u in users}
  diffs = []
  import datetime as dt
  diffs_total = dt.timedelta()
  for user, last in last_runs.items():
    registered = users[user]['t_created']
    registered = datetime.strptime(registered,'%Y-%m-%d %H:%M:%S.%f%Z')
    last_runs[user] = (registered, last)
    diffs.append(last-registered)
    diffs_total += diffs[-1]

  diffs = sorted(diffs)
  print(f"Average time from register to last question: {(diffs_total/len(diffs))}")
  print(len(diffs))
  print(f"Median time: {diffs[int(len(diffs)/2)]}")
  print(f"Fastest: {diffs[0]}")
  print(f"Slowest: {diffs[-1]}")




if __name__ == "__main__":
  get_data()
