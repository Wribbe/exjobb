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

  qs = [
    "What are your feelings on the current taks assigning and tracking system?",
    "Anything in particular that works well?",
    "Could something be improved?",
    "Is there anything missing that you would like to have?",
    "Are there gaps in the information you receive? What could be added? Why?",
  ]

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

  @app.route("/sum/questions")
  def questions_sum():
    sums = [
      [
        """
        Tracking works well when the information is entered in Shotgun correctly.
        There are lingering ephemeral tasks that never get entered into Shotgun
        correctly, they exist on a todo somewhere or as an verbal agreement
        over something.
        """,
        """
        Can be hard to track tasks related to work that overlap different
        departments, since they can end up in different systems.
        """,
        """
        It is functional but could be more user friendly. If things are moving
        too fast it is easily abandoned.
        """,
      ],
      [
        """
        It is secure and retains data without any loss.
        """,
        """
        Easy to get an overview of who is working on what (though it does only
        works if people update it correctly). It is easy to create recurring
        tasks through task templates.
        """,
        """
        Notification system for changes on character tasks works well when you
        notice them.
        """,
        """
        Good integration with Snowdrop and Quality Control.
        """,
      ],
      [
        """
        Making it more user friendly in order to make it easier to incorporate.
        """,
        """
        Templates solves recurring task but still lot of work for unique tasks.
        """,
        """
        Better communication around tasks, threads or similar.
        """,
        """
        Easier tracking of time spent on tasks and logging.
        """,
        """
        There is no way to see the total workload in either system or the work
        present in them combined.
        """,
        """
        Feed back actual time spent into the proposed bid for adjustment.
        """,
        """
        Easier communication between teams.
        """,
        """
        Consolidate things that currently live in different places.
        """,
      ],
      [
        """
        Other input streams for task creation, e.g. email to task.
        """,
        """
        Different, personalized ways of viewing different task and todos, e.g.
        GTD.
        """,
        """
        Shotgun-Jira bridge that mirrors information between both.
        """,
        """
        Additional status page with filters.
        """,
        """
        Visualization of the whole teams current work.
        """,
      ],
      [
        """
        A way to distribute the state of the current movie in a playable format
        with others in the organization.
        """,
        """
        Better overview.
        """,
        """
        A way to schedule task based on dependencies.
        """,
        """
        Combine task information together with other system, e.g. vacation
        information from other systems.
        """,
      ]
    ]
    if len(sums) < len(qs):
      sums += [[]]*(len(qs)-len(sums))
    html, pdf = render_template(
      "questions/01_sum.html",
      styles=[
#        "style_pitch.css",
        "style_questions.css",
      ],
      questions = zip(qs, sums),
    )
    return html

  def _questions(hide_pdf=False):
#    qs = [
##      "What is your position?",
#      "Do any of your current tasks involve manually drawing conclusions based on data that live in different places?",
#      "Is there a tasks that is made harder by a lacking or cumbersome user interface?",
#      "If you could wish a currently missing, feasible, data-stream into existence to make your work easier, what would it be?",
#      "Do you have a tasks that would become easier if the data involved was organized or filtered in a different way?",
#      "Is there a task that you feel could be automated?",
#      "Do any of your tasks involve assembling data for others to view?"
#    ]
    fields = [
      "ANON-ID",
#      "Name",
#      "Age",
#      "Gender",
      "Date",
      "Time Start",
      "Time End",
    ]
    html, pdf = render_template(
      "questions/01.html",
      styles=[
#        "style_pitch.css",
        "style_questions.css",
      ],
      fields = fields,
      questions = qs + ['Notes'],
      hide_pdf=hide_pdf,
    )
    return html, pdf

  @app.route("/questions/01")
  def questions():
    html, pdf = _questions()
    return html

  @app.route("/questions/01/pdf")
  def questions_pdf():
    html, pdf = _questions(hide_pdf=True)
    resp = Response(pdf)
    resp.mimetype = 'application/pdf'
    return resp

  def _anon(hide_pdf=False):
    num_people = 30
    fields = [
      'ANON-ID',
      'Name',
      'Position',
      'Age',
      'Gender',
    ]
    html, pdf = render_template(
      "questions/anon.html",
      styles=[
        "style_pitch.css",
        "style_anon.css",
      ],
      fields = fields,
      num_people = num_people,
      hide_pdf=hide_pdf,
    )
    return html, pdf

  @app.route("/anon")
  def anon():
    html, pdf = _anon()
    return html

  @app.route("/anon/pdf")
  def anon_pdf():
    html, pdf = _anon(hide_pdf=True)
    resp = Response(pdf)
    resp.mimetype = 'application/pdf'
    return resp

  @app.route("/gantt")
  def gantt():
    return render_template(
      "gantt.html",
      styles=[]
    )[0]

  @app.route("/logs/")
  def logs():
    paths = [
      os.path.basename(p)
      for p in os.listdir(os.path.join(app.static_folder, 'logs'))
    ]
    paths = [(p.split('.')[0], p) for p in paths]
    return render_template(
      'logs.html',
      paths=paths,
    )[0]
  return app
