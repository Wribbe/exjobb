import sqlite3
from pathlib import Path
import itertools
import matplotlib as plt

from datetime import datetime

order = [
  'employee hours',
  'team workload',
  'task dependencies',
  'team performance'
]

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
  hashchars = ['\\','.','/','x','o','*']
  hatchings = [''] + [c*5 for c in hashchars]
  markers = {
    'plot': ['o-', 'v--', 'x:', '+-.'],
    'barh': hatchings,
    'bar': hatchings,
  }
  return itertools.cycle(markers.get(method, [""]))


iter_colors = itertools.cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])

def run_to_datetimes(run):
  fmt = "%Y-%m-%d %H:%M:%S.%f%Z"
  start, stop = run['t_start'], run['t_stop']
  return [datetime.strptime(d, fmt) for d in [start, stop]]

figure_units = {
  'size': (0.7*8.3, 2.3),
}

def figure_setup(figure, size=figure_units['size']):
  figure.set_size_inches(size)
  figure.tight_layout()

def figure_save(figure, path_out):
  figure.savefig(path_out, bbox_inches='tight')
