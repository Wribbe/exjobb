#!/usr/bin/env python

import time
import subprocess

from pathlib import Path
to_watch = [Path('msccls','report.tex')]
last_seen = {}

def file_changed(path):
  modded_at = path.stat().st_mtime
  if not last_seen.get(path):
    last_seen[path] = modded_at
    return False
  if modded_at != last_seen[path]:
    last_seen[path] = modded_at
    return True


print(f"watching {','.join([str(p) for p in to_watch])}")
while True:
  for watch in to_watch:
    if file_changed(watch):
      subprocess.call('make')
    break
  time.sleep(1)
