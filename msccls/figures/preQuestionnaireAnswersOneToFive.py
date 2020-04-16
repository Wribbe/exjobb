from msccls.figures.utils import *

import numpy as np
import matplotlib.pyplot as plt


category_names = [
  'Strongly disagree',
  'Disagree',
  'Neither agree nor disagree',
  'Agree',
  'Strongly agree'
]



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
#  q_final = {
#    'age': 'age',
#    'identifies': 'identifies as',
#    'screen_size': 'screen size',
#    'device_type': 'input type',
#  }
#
#  categories = {
#    'identifies': ['female','male','other'],
#    'device_type': ['mouse','trackpad','touch','other'],
#    'screen': ['desktop','laptop','tablet','mobile'],
#  }

  ans_data_per_q = {}
  for q,aans in answers_per_question.items():
    if not q.startswith('I'):
      continue
    q = ' '.join([l.strip() for l in q.splitlines()])
    for a in aans:
      a = int(a['answer'])
      ans_data_per_q.setdefault(q, {})
      ans_data_per_q[q].setdefault(a, 0)
      ans_data_per_q[q][a] += 1


  results = {}
  for n, (q, d) in enumerate(ans_data_per_q.items(), start=1):
    for i in range(1,6):
#      if not d.get(i):
#        continue
      results.setdefault(f"Q{n}", []).append(d.get(i, 0))

  results = {'Q1': results['Q1']}
#  results_old = {
#    'Q1': [10, 15, 17, 32, 26],
#    'Q2': [10, 10, 10, 26, 13],
#    'Q3': [35, 37, 7, 2, 19],
#    'Q4': [32, 11, 9, 15, 33],
#    'Q5': [21, 29, 5, 5, 40],
#    'Q6': [8, 19, 5, 30, 38],
#  }

#  from pprint import pprint
#  pprint(results)
#  pprint(results_old)

#  print(results)


  labels = list(results.keys())
  data = np.array(list(results.values()))
  data_cum = data.cumsum(axis=1)
  category_colors = plt.cm.get_cmap('RdYlGn')(
    np.linspace(0.15, 0.85, data.shape[1]))

  fig, ax = plt.subplots(figsize=(9.2, 1))
  ax.invert_yaxis()
  ax.xaxis.set_visible(False)
  ax.set_xlim(0, np.sum(data, axis=1).max())

  for i, (colname, color) in enumerate(zip(category_names, category_colors)):
    widths = data[:, i]
    starts = data_cum[:, i] - widths
    ax.barh(labels, widths, left=starts, height=0.5,
            label=colname, color=color)
    xcenters = starts + widths / 2

    r, g, b, _ = color
    text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
    for y, (x, c) in enumerate(zip(xcenters, widths)):
      if not int(c):
        continue
      ax.text(x, y, str(int(c)), ha='center', va='center',
              color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
  plt.yticks([])

#  fig.set_size_inches(figure_units['size'])
#  plt.xlabel('First second and onwards')
#  plt.ylabel('Units in group')
#  plt.title('Histogram of completion times, Employee Hours')
  #fig.tight_layout()
  #figure_setup(fig)
  figure_save(fig, path_out)
