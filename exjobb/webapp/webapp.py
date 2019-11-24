import exjobb.config as config
config.virt_load()

import flask
import os
import sqlite3
import random
import json

DATABASE = 'test_db.db'

from pathlib import Path
from flask_weasyprint import render_pdf, HTML
from flask import \
  Response, request, redirect, url_for, session, g, send_from_directory

import datetime
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
  app.secret_key = 'aosit2o3i8ls-[3-[svocx.vk,asrtn33'

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

  @app.route("/logs/<filename>")
  def logs(filename):
    return send_from_directory(os.path.join('static','logs'), filename)

  @app.route("/test/results")
  def results_test():
    cur = get_db().execute('select * from tests')
    res = [(
        r['key'],
        (datetime.datetime.fromtimestamp(float(r['stop'])) -
        datetime.datetime.fromtimestamp(float(r['start']))).seconds
      ) for r in cur.fetchall()
    ]
    cur.close()
    return render_template(
      "test/results.html",
      results = res,
    )[0]

  sql_create = "INSERT INTO tests (key, start) VALUES (?, ?)"
  sql_update_stop = lambda id_test,stop: \
    f"UPDATE tests SET stop = '{stop}' WHERE key = '{id_test}'"

  @app.route("/test/<id_test>", methods=['GET','POST'])
  def test(id_test):
    cur = get_db().cursor()
    if request.method == "POST":
      now = datetime.datetime.now().timestamp()
      cur.execute(sql_update_stop(id_test, now))
      get_db().commit()
      cur.close()
      return redirect(url_for('results_test'))
    now = datetime.datetime.now().timestamp()
    try:
      cur.execute(sql_create, (id_test, now))
    except sqlite3.IntegrityError as e: # Already exists.
      pass
    get_db().commit()
    cur.close()
    buttons = [False]*10 + [True]
    circles = [False]*4 + [True]
    random.shuffle(buttons)
    random.shuffle(circles)

    return render_template(
      'test/test.html',
      id_test=id_test,
      buttons=buttons,
      circles=circles,
      styles=['style_test.css'],
    )[0]

  alph = list('abcdefghijklmnopqrstuvwxyz')
  @app.route("/test/list")
  def tests_list():
    ids = [(alph[i].upper())*3 for i in range(0,5)]
    return render_template(
      'test/test_list.html',
      ids=ids
    )[0]

  def get_db():
    db = getattr(g, '_database', None)
    if not db:
      db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

  @app.teardown_appcontext
  def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
      db.close()


  @app.route("/pdf/<pdf_id>")
  def send_pdf(pdf_id):
    return send_from_directory(Path(app.static_folder, 'pdf'), pdf_id)

  @app.route("/mockup/<int:batch>/<int:version>")
  def mockup(batch, version):

    font_size = 20
    bufferx= 17
    buffery= 21
    out = [
      '<svg width="297mm" height="210mm" xmlns="http://www.w3.org/2000/svg">',
      '<style>',
      '  .heavy { font: bold 40px; }',
      '</style>',
    ]

    buttons = ["Hours","Availability", "Dependencies", "Performance"]


    def button(x,y,width,height,text,rx=0,anchor="middle",left=False):
      out = []
      textx = x+(width/2.0)
      texty = y+(height/2.0)+font_size/2.5
      out.append(
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}"'+\
        f' rx="{rx}" fill="white" stroke="black"/>'
      )
      out.append(
        f'<text x="{textx}" y="{texty}" font-size="{font_size}"'+\
        f' text-anchor="{anchor}">{text}</text>'
      )
      return os.linesep.join(out)

    def workarea(x,y,width,height,text="Data View",font_size=50):
      textx = x+(width/2.0)
      texty = y+(height/2.0)+font_size/2.5
      anchor = "middle"
      out = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}"'+\
        f' fill="white" stroke="black" stroke-dasharray="4"/>'
      ]
      out.append(
        f'<text x="{textx}" y="{texty}" font-size="{font_size}"'+\
        f' text-anchor="{anchor}" fill="black">{text}</text>'
      )
      return os.linesep.join(out)

    def mark(text):
      text = str(text)
      return \
        f'<text x="1050" y="60" class="heavy" text-anchor="middle">{text}</text>'

    if version == 1:
      sumx = 0
      for i, text in enumerate(buttons):
        width = len(text)*font_size
        out.append(button(bufferx+sumx,buffery,width,50,text))
        sumx += (width + 10)
      out.append(workarea(bufferx,buffery+60,1080,615))
      out.append(
        workarea(bufferx,710,1080,60,text="Additional Info",font_size=30)
      )
    if version == 2:
      sumx = 0
      for i, text in enumerate(buttons):
        width = len(text)*font_size
        out.append(button(bufferx+sumx,buffery,width,50,text))
        sumx += (width + 10)
      out.append(workarea(bufferx,buffery+60,830,680))
      out.append(
        workarea(bufferx+830+20,buffery+50+10,230,680,text="Additional Info",font_size=25)
      )
    if version == 3:
      size_max = max([len(b) for b in buttons])
      width = size_max*font_size
      for i, text in enumerate(buttons):
        out.append(button(bufferx,buffery+(60*i),width,50,text,left=True))
      out.append(workarea(bufferx+width+20,buffery,820,670))
      out.append(
        workarea(bufferx,710,1080,60,text="Additional Info",font_size=30)
      )
    if version == 4:
      size_max = max([len(b) for b in buttons])
      width = size_max*font_size
      for i, text in enumerate(buttons):
        out.append(button(bufferx,buffery+(60*i),width,50,text,left=True))
      out.append(workarea(bufferx+width+20,buffery,820,740))
      out.append(
        workarea(bufferx,buffery+(60*len(buttons))+20,width,480,text="Additional Info",font_size=30)
      )

    out.append(mark(f"{batch}.{version}"))
    out.append("</svg>")
    return os.linesep.join(out)

  @app.route('/ui/<version>')
  def ui(version):

    version_select = {
      # (Button-are-vertical, additional-pos).
      '1.1': (False,"B"),
      '1.2': (False,"R"),
      '1.3': (True,"B"),
      '1.4': (True,"L"),
    }

    vers = version_select.get(version)
    if not vers:
      return f"No such ui-version: {version}."

    buttons_vertical, pos_additional = vers

    classes = []

    buttons = [
      "Hours",
      "Availability",
      "Dependencies",
      "Performance",
    ]
    views = [
      "view-data",
      "view-additional"
    ]

    view_data = {
      'name': "view-data",
    }
    view_additional = {
      'name': "view-additional",
    }


    if buttons_vertical:
      size_view_data = (605, 605)
      for i, button in enumerate(buttons, start=1):
          classes.append(
            {
              'name': f"{button}",
              'col': "1/3",
              'row': "{i}",
            }
          ),
    else:
      for i, button in enumerate(buttons, start=1):
        classes.append(
          {
            'name': f"{button}",
            'col': f"{i}",
            'row': "1",
          }
        )

    if pos_additional == "R":

      size_view_data = (620, 430)
      view_additional['col'] = '7/10'
      view_additional['row'] = '2/20'

      view_data['col'] = '1/7'
      view_data['row'] = '2/20'

    elif pos_additional == "B":

      if buttons_vertical:

        size_view_data = (590, 570)
        view_additional['col'] = '1/10'
        view_additional['row'] = '19/20'

        view_data['col'] = '3/10'
        view_data['row'] = '1/19'

      else:

        size_view_data = (800, 400)
        view_additional['col'] = '1/10'
        view_additional['row'] = '19/20'

        view_data['col'] = '1/10'
        view_data['row'] = '2/19'

    elif pos_additional == "L":

      size_view_data = (590, 600)
      view_additional['col'] = '1/3'
      view_additional['row'] = '5/20'

      view_data['col'] = '3/10'
      view_data['row'] = '1/20'


#      .one {
#        grid-column: 1/3;
#        grid-row: 1;
#      }
#
#      .two {
#        grid-column: 2/4;
#        grid-row: 1/3;
#      }
#      .three {
#        grid-column: 1;
#        grid-row: 2/6;
#      }
#      .four {
#        grid-column: 3;
#        grid-row: 3;
#      }

    classes.append(view_data)
    classes.append(view_additional)

    return render_template(
      "ui/main.html",
      classes=classes,
      buttons=buttons,
      views=views,
      size_view_data=size_view_data,
    )[0]

  @app.route('/data/ui/<mode>')
  def data_ui(mode):
    return json.dumps({'name': mode})

  @app.route('/cards')
  def cards():
    font_size = 35
    bufferx= 17
    buffery= 21

    def button(x,y,width,height,text,rx=0,anchor="middle",left=False):
      nonlocal font_size
      old_size = font_size
      if type(text) == tuple:
        text, font_size = text
      out = []
      textx = x+(width/2.0)
      texty = y+(height/2.0)+font_size/2.5
      out.append(
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}"'+\
        f' rx="{rx}" fill="white" stroke="black"/>'
      )
      out.append(
        f'<text x="{textx}" y="{texty}" font-size="{font_size}"'+\
        f' text-anchor="{anchor}">{text}</text>'
      )
      font_size = old_size
      return os.linesep.join(out)

    out = [
      '<svg width="297mm" height="210mm" xmlns="http://www.w3.org/2000/svg">',
      '<style>',
      '  .heavy { font: bold 40px; }',
      '</style>',
    ]
    card_width = 350
    card_height = 178

    cards = [
      "Clarity",
      "Discriminability",
      "Conciseness",
      "Consistency",
      "Detectability",
      "Legibility",
      "Comprehensibility",
      "Effectiveness",
      "Efficiency",
      "Satisfaction",
    ]

#Suitability for the task
#Self-descriptiveness
#Controllability
#Conformity with user expectations
#Error tolerance
#Suitability for individualization
#Suitability for learning

    for j in range(4):
      for i in range(3):
        index = j*3+i
        try:
          txt = cards[index]
        except:
          txt = index
        out.append(
          button(
            bufferx+(card_width+10)*i,
            buffery+(card_height+10)*j,
            card_width,
            card_height,
            txt,
          )
        )
    out.append('</svg>')
    return os.linesep.join(out)

  @app.route('/presentation')
  def presentation():
    header = """
    <div class="header">
      <div>Header</div>
    </div>
    """
    footer = """
    <div class="footer">
      <div>Footer</div>
    </div>
    """
    html, pdf = render_template(
      "presentation.html",
      header=header,
      footer=footer,
    )
    with open('test.pdf', 'wb') as fh:
      fh.write(pdf)
    return html

  @app.route('/report')
  def report():
    return "Report"

  return app
