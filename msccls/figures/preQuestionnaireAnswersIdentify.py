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

  t = 'identifies as'
  cs = list(reversed(['Female','Male','Other']))

  categories = {
    k:0 for k in ans_data_per_q[t]
  }

  for cat, num in ans_data_per_q[t].items():
    categories[cat] += int(num)

  fig, ax = plt.subplots()


  color = iter_colors.__next__()
  for y, cat in enumerate(cs, start=1):
    num = categories[cat]
    plt.plot(range(1, num+1), [y]*num, 'o', color=color)

  yticks = range(1, len(categories)+1)
  plt.yticks(yticks, [c.title() for c in cs])
  plt.xlabel('Number of participants in category')
  plt.ylabel('Identifies as')
  plt.title('Participants identifies as')
  plt.ylim(0, len(categories)+1)
  figure_setup(fig)
  figure_save(fig, path_out)
