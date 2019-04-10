import exjobb.config as cfg
cfg.virt_load()

import flask
import os

from flask_weasyprint import render_pdf

app = flask.Flask(__name__)

def run():
  os.environ["FLASK_APP"] = __name__
  os.environ["FLASK_ENV"] = "development"
  cfg.call("flask run")
