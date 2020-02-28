from msccls.figures.utils import *

import matplotlib.pyplot as plt
import numpy as np

def get_data(path_out):

  db = get_db()
  answers = db.execute("SELECT * FROM answer").fetchall()
  db.close()

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

  ranges = [
    (0,20),
    (21,25),
    (26,30),
    (31,35),
    (36,40),
    (41,100),
  ]

  range_to_string = lambda t: f"{t[0]}-{t[-1]}" if t[-1]<100 else f"{t[0]}+"
  categories = {
    range(a,b+1): 0 for a,b in ranges
  }
  for age, num in ans_data_per_q['age'].items():
    for cat in categories:
      if int(age) in cat:
        categories[cat] += int(num)
        break

  fig, ax = plt.subplots()

  color = iter_colors.__next__()
  for y, (category, num) in enumerate(categories.items(), start=1):
    plt.plot(range(1, num+1), [y]*num, 'o', color=color)

  yticks = range(1, len(categories)+1)
  ylabels = [range_to_string(c) for c in categories]
  plt.yticks(yticks, ylabels)
  plt.xlabel('Number of participants in in category')
  plt.ylabel('Age ranges')
  plt.title('Participant age-ranges')
  plt.ylim(0, 7)
  figure_setup(fig)
  figure_save(fig, path_out)
