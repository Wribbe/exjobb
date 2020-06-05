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

def main():

  run_list = [
    db_update,
  ]

  ret, args, kwargs = [[], [], {}]
  for m in run_list:
    ret, args, kwargs = m(*args, **kwargs)

if __name__ == "__main__":
  main()
