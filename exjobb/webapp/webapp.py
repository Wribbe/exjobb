import exjobb.config as cfg
cfg.virt_load()

import flask
import os

from flask_weasyprint import render_pdf, HTML
from flask import Response
import weasyprint

app = flask.Flask(__name__)

DIR_OUT = os.path.join("exjobb", "out")

def render_template(template, **data):
  html = flask.render_template(template, **data)
  name_out = os.path.join(*os.path.split(template))
  name_out = name_out.replace(".html", ".pdf")
  pdf = save_pdf(html, os.path.join(DIR_OUT, name_out))
  return (html, pdf)

def save_pdf(string_html, path):
  path_dir = os.path.dirname(path)
  if path_dir and not os.path.exists(path_dir):
    os.makedirs(path_dir)
  obj_html = HTML(string=string_html)
  data_pdf = obj_html.write_pdf()
  with open(path, 'wb') as fh:
    fh.write(data_pdf)
  return data_pdf

@app.route("/")
def index():
  return render_template("main/00_title.html")[0]

@app.route("/main")
def main():
  html_final = []
  for name in sorted(os.listdir('exjobb/webapp/templates/main')):
    html_final.append(render_template(f"main/{name}")[0])
  html_final = "<br>".join(html_final)
  save_pdf(html_final, os.path.join(DIR_OUT, "main", "main.pdf"))
  return html_final

@app.route("/presentation")
def presentation():
  return render_template(
    "presentation/01.html",
    styles=["style_presentation.css"]
  )[0]

@app.route("/presentation/slides_render")
def presentation_slides_render():
  return render_template(
    "presentation/01.html",
    styles=[
      "style_presentation.css",
      "style_presentation_slides.css",
    ]
  )[0]

@app.route("/presentation/slides")
def presentation_slides():
  pdf = render_template(
    "presentation/01.html",
    styles=[
      "style_presentation.css",
      "style_presentation_slides.css",
    ]
  )[1]
  resp = Response(pdf)
  resp.mimetype = 'application/pdf'
  return resp

def run():
  os.environ["FLASK_APP"] = __name__
  os.environ["FLASK_ENV"] = "development"
  cfg.call("flask run --host=0.0.0.0 --port=8000")
