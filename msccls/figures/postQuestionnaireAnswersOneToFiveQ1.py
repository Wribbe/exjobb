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

  ans_data_per_q = {}
  for q,aans in answers_per_question.items():

    if q.startswith('I'):
      continue
    if q in questions:
      continue
    if q.startswith('addit'):
      continue

    q = ' '.join([l.strip() for l in q.splitlines()])
    for a in aans:
      if not a:
        continue
      a = int(a['answer'])
      ans_data_per_q.setdefault(q, {})
      ans_data_per_q[q].setdefault(a, 0)
      ans_data_per_q[q][a] += 1

  all_results = {}
  for n, (q, d) in enumerate(ans_data_per_q.items(), start=1):
    for i in range(1,6):
      all_results.setdefault(f"Q{n}", []).append(d.get(i, 0))

  def get_fig(num, path_out):
    results = {f'Q{num}': all_results[f'Q{num}']}

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

      path_out = str(path_out)[:-5] + f"{num}.pdf"
      figure_save(fig, path_out)

  for i in range(1, len(all_results)+1):
    get_fig(i, path_out)
