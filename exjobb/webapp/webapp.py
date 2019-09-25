import exjobb.config as config
config.virt_load()

import flask
import os

from flask_weasyprint import render_pdf, HTML
from flask import Response
import weasyprint

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

def create_app():

  app = flask.Flask(__name__)

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

  @app.route("/pitch")
  def pitch():
    return render_template(
      "pitch/01.html",
      styles=["style_pitch.css"]
    )[0]

  @app.route("/goaldocument")
  def goaldoc():
    return render_template(
      "goaldoc.html",
      styles=["style_goal.css"],
    )[0]

  @app.route("/goaldocument/pdf")
  def pdf_goaldoc():
    pdf = render_template(
      "goaldoc.html",
      styles=[
        "style_goal.css",
        "style_goal_pdf.css",
        "style.css",
      ],
    )[1]
    resp = Response(pdf)
    resp.mimetype = 'application/pdf'
    return resp

  @app.route("/pitch/slides_render")
  def pitch_slides_render():
    return render_template(
      "pitch/01.html",
      styles=[
        "style_pitch.css",
        "style_pitch_slides.css",
      ]
    )[0]

  @app.route("/pitch/slides")
  def pitch_slides():
    pdf = render_template(
      "pitch/01.html",
      styles=[
        "style_pitch.css",
        "style_pitch_slides.css",
      ]
    )[1]
    resp = Response(pdf)
    resp.mimetype = 'application/pdf'
    return resp

  @app.route("/questions/01")
  def questions():
    qs = [
#      "What is your position?",
      "Do any of your current tasks involve manually drawing conclusions based on data that live in different places?",
      "Is there a tasks that is made harder by a lacking or cumbersome user interface?",
      "If you could wish a currently missing, feasible, data-stream into existence to make your work easier, what would it be?",
      "Do you have a tasks that would become easier if the data involved was organized or filtered in a different way?",
      "Is there a task that you feel could be automated?",
      "Do any of your tasks involve assembling data for others to view?"
    ]
    html, pdf = render_template(
      "questions/01.html",
      styles=[
        "style_pitch.css",
      ],
      questions=qs,
    )
    return html

  @app.route("/gantt")
  def gantt():
    return render_template(
      "gantt.html",
      styles=[]
    )[0]

  return app
