import os
import subprocess
import venv
import shutil

DIR_VIRT = "virt_py3"
DIR_VIRT_BIN = os.path.join(DIR_VIRT, "bin")

PATH_VIRT_ACTIVATE = os.path.join(DIR_VIRT_BIN, "activate_this.py")

PY = os.path.join(DIR_VIRT_BIN, "python")

def call(command):
  if type(command) == str:
    command = command.split()
  return subprocess.call(command)

def virt_create():
  if not os.path.exists(DIR_VIRT):
    venv.create(DIR_VIRT, with_pip=True)
    call(f"{PY} -m pip install -r requirements.txt")
    shutil.copy(
      os.path.join("scripts", "activate_this.py"),
      PATH_VIRT_ACTIVATE
    )

def virt_load():
  exec(
    compile(
      open(PATH_VIRT_ACTIVATE, 'rb').read(),
      PATH_VIRT_ACTIVATE,
      'exec'
    ),
    dict(__file__=PATH_VIRT_ACTIVATE)
  )

def run():
  virt_create()
  virt_load()
  print("Running!")
