import sqlite3
from pathlib import Path
import itertools
import matplotlib as plt

def get_db():
  path_dir = Path(__file__).parents[2]
  db_name = 'db2.sqlite3.db'
  db = sqlite3.connect(Path(path_dir, db_name))
  db.row_factory = sqlite3.Row
  return db


def run_successful(run):
  run = dict(run)
  if run.get('success') == 1:
    return True
  if run.get('answer') == run.get('answer_correct'):
    return True
  return False


def incremental_sum(dic):
  y_sum = 0
  xs, ys = ([], [])
  for x, y in sorted(dic.items()):
    xs.append(x)
    y_sum += y
    ys.append(y_sum)
  return (xs,ys)


def dump_vars(vs):

  path_vars = Path(Path(__file__).parents[2], 'vars')
  if not path_vars.is_dir():
    path_vars.mkdir()

  if not type(vs) == list:
    vs = [vs]

  for name, value in vs:
    path_out = Path(path_vars, f"{name}.txt")
    path_out.write_text(f"{value}")


def as_percent(f):
  return rf"$\sim${f:.1f}\%"


def iter_markers(method):
  hashchars = ['\\','/','x','o','.',':','*']
  hatchings = [''] + [c*5 for c in hashchars]
  markers = {
    'plot': ['o-', 'v--'],
    'barh': hatchings,
    'bar': hatchings,
  }
  return itertools.cycle(markers[method])


def iter_colors():
  return itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
