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

  t = 'input type'
  cs = list(reversed(['Mouse','Trackpad','Touch','Other']))

  categories = {
    k:0 for k in ans_data_per_q[t]
  }

  for cat, num in ans_data_per_q[t].items():
    categories[cat] += int(num)

  fig, ax = plt.subplots()


  color = iter_colors.__next__()
  xticks = range(1, max(categories.values())+1)
  ax.vlines(xticks[1::2], 0, len(categories)+1, alpha=0.3, linestyles='dotted', linewidth=1,
                zorder=-20)
  ax.vlines(xticks[::2], 0, len(categories)+1, alpha=0.1, linestyles='dotted',
            linewidth=1,
                zorder=-20)
  for y, cat in enumerate(cs, start=1):
    num = categories[cat]
    plt.plot(range(1, num+1), [y]*num, 'o', color=color)

  yticks = range(1, len(categories)+1)
  plt.yticks(yticks, [c.title() for c in cs])
  plt.title('Input devices used by participants')
  plt.xlabel('Number of participants in category')
  plt.ylabel('Input types')
  plt.ylim(0, len(categories)+1)
  figure_setup(fig)
  figure_save(fig, path_out)
