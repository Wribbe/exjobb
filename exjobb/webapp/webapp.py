import exjobb.config as cfg
cfg.virt_load()

import flask
import os

from flask_weasyprint import render_pdf, HTML
from flask import render_template
import weasyprint

app = flask.Flask(__name__)

DIR_OUT = os.path.join("exjobb", "data", "images")

def save_pdf(name_html, name):
  if not os.path.exists(DIR_OUT):
    os.makedirs(DIR_OUT)
  html = HTML(string=render_template(name_html))
  html.write_pdf(os.path.join(DIR_OUT, name))

@app.route("/")
def hello():
  html = render_template("test.html")
  save_pdf("test.html", "test.pdf")
  return html

def run():
  os.environ["FLASK_APP"] = __name__
  os.environ["FLASK_ENV"] = "development"
  cfg.call("flask run")
