#!/usr/bin/env python

import json
import os
import re
import shlex
import sqlite3
import subprocess
import sys

from pathlib import Path

PATH_CONF=Path('sync_db.json')

def call(cmd):
  print(f"Running: {cmd}")
  return subprocess.call(shlex.split(cmd))

def db_update():
  keys = ['remote', 'port', 'path']
  dest = Path('./msccls')
  if not PATH_CONF.is_file():
    conf = {k:input(f"{k}?: ") for k in keys}
    PATH_CONF.write_text(json.dumps(conf, indent=2))

  conf = json.loads(PATH_CONF.read_text())
  remote, port, path = [conf[k] for k in keys]
  call(f'rsync -avzz -e "ssh -p {port}" {remote}:{path}/*.db {dest}')
  path_db = [Path(f) for f in os.listdir(dest) if f.endswith('.db')][0]
  path_db = Path(dest, path_db).resolve()
  return ("", [path_db], {})

def db_dump_data(db_src):
  print(f"Working on: {db_src}")
  path_data_figures = Path("msccls", "data_figures")
  if not path_data_figures.is_dir():
    path_data_figures.mkdir()
  db = sqlite3.connect(db_src)
  db.row_factory = sqlite3.Row
  cursor = db.cursor()

  def dump_to_disk(parsing_code, name, data):

    min_indent = min([
      len(re.findall(r'^\s+', line)[0])
      for line in parsing_code.splitlines() if line.strip()
    ])
    parsing_code = ';'.join(
      [l[min_indent:] for l in parsing_code.splitlines() if l.strip()]
    )

    names_keys = {
      't_created': 'time_created',
      'str_id': 'id_user',
    }

    path = Path(path_data_figures, f"{name}.csv")
    if not path.is_file():
      path.touch()
    keys = data[0].keys()
    header = ','.join([names_keys.get(k, k) for k in keys])
    data = [','.join([str(obj[k]) for k in keys]) for obj in data]
    current = path.read_text()
    final_data = os.linesep.join([parsing_code, header] + data)
    if current == final_data:
      return
    path.write_text(final_data)

  def num_participants(name_output):
    data = cursor.execute('SELECT t_created, str_id FROM test_user').fetchall()
    parsing_code = """
      dates = {}
      for line in data:
        time, id = line.split(',', 1)
        date = time.split(' ')[0]
        dates.setdefault(date, 0)
        dates[date] += 1
      sum = 0
      x, y = [[], []]
      for date, num_ids in sorted(dates.items()):
        x.append(date)
        sum += num_ids
        y.append(sum)
      datasets.append((x, y))
    """
    dump_to_disk(parsing_code, name_output, data)

  def num_runs(name_output):
    data = cursor.execute('SELECT t_start, id, t_stop, success FROM test_run').fetchall()
    parsing_code = """
      dates = {}
      dates_complete = {}
      dates_success = {}
      for line in data:
        time, id, t_stop, success = line.split(',')
        date = time.split(' ')[0]
        dates.setdefault(date, 0)
        dates[date] += 1
        if not t_stop.strip():
          dates_complete.setdefault(date, 0)
          dates_complete[date] += 1
        if bool(int(success)):
          dates_success.setdefault(date, 0)
          dates_success[date] += 1
      sum = 0
      x, y = [[], []]
      for date, num_ids, in sorted(dates.items()):
        x.append(date)
        sum += num_ids
        y.append(sum)
      datasets.append((x, y))

      sum = 0
      x, y = [[], []]
      for date, num_ids in sorted(dates_complete.items()):
        x.append(date)
        sum += num_ids
        y.append(sum)
      datasets.append((x, y))

      sum = 0
      x, y = [[], []]
      for date, num_ids in sorted(dates_success.items()):
        x.append(date)
        sum += num_ids
        y.append(sum)
      datasets.append((x, y))
    """
    dump_to_disk(parsing_code, name_output, data)

  outputs = {
    "participants_over_time": num_participants,
    "runs_over_time": num_runs,
  }

  for name, method in outputs.items():
    method(name)

  db.close()
  return ("", [], {})

def main():

  run_list = [
    db_update,
    db_dump_data,
  ]

  ret, args, kwargs = [[], [], {}]
  for m in run_list:
    ret, args, kwargs = m(*args, **kwargs)

if __name__ == "__main__":
  main()
