import exjobb.config as cfg
cfg.virt_load()

import flask
import os

from flask_weasyprint import render_pdf, HTML
#from flask import render_template
import weasyprint

app = flask.Flask(__name__)

DIR_OUT = os.path.join("exjobb", "out")

def render_template(template, *data):
  html = flask.render_template(template, *data)
  name_out = os.path.join(*os.path.split(template))
  name_out = name_out.replace(".html", ".pdf")
  save_pdf(html, name_out)
  return html

def save_pdf(string_html, name):
  if not os.path.exists(DIR_OUT):
    os.makedirs(DIR_OUT)
  obj_html = HTML(string=string_html)
  with open(os.path.join(DIR_OUT, name), 'wb') as fh:
    fh.write(obj_html.write_pdf())

@app.route("/")
def index():
  return render_template("main/00_title.html")

def run():
  os.environ["FLASK_APP"] = __name__
  os.environ["FLASK_ENV"] = "development"
  cfg.call("flask run")
