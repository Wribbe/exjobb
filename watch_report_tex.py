#!/usr/bin/env python

import time
import subprocess
import os

from pathlib import Path
to_watch = Path('msccls')
last_seen = {}

def file_changed(path):
  modded_at = path.stat().st_mtime
  if not last_seen.get(path):
    last_seen[path] = modded_at
    return False
  if modded_at != last_seen[path]:
    last_seen[path] = modded_at
    return True

def something_changed(files):
  for file in files:
    if not file.endswith(".tex") and not file.endswith(".bib"):
      continue
    path = Path(root, file)
    if file_changed(path):
      return True
  return False

print(f"watching {to_watch}")

while True:

  for root, _, files in os.walk(to_watch):
    if something_changed(files):
      subprocess.call('make')
      break
  time.sleep(1)
