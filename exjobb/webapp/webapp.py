import exjobb.config as config
config.virt_load()

import flask
import os
import sqlite3
import random
import json
import math

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


  title = "Measuring UI-/UX-impact on task efficiency"

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
      title=title,
    )
    with open('presentation.pdf', 'wb') as fh:
      fh.write(pdf)
    return html

  def toc_generate(html):
    buffer = []
    num = [0]*10
    headings = [f"h{i}" for i in range(1,5)]
    page = 0
    toc = {}

    for line in html.splitlines():

      if 'class="page' in line:
        page += 1

      tag = line.split('>', 1)[0]
      for ending in headings:
        if tag.endswith(ending):
          level = int(ending[1:])
          a,b = line.split('>',1)
          b,c = b.split('<',1)
          if b.startswith('**'):
            b = b[2:]
            line = f"{a}>{b}<{c}"
            break
          elif b.startswith('*'):
            b = b[1:]
            toc.setdefault(page, []).append(
              f"<span class='toc-line toc-{level}'>{b}</span>"+\
              f"<span class='toc-pagenumber'>{page}</span>"
            )
            line = f"{a}>{b}<{c}"
            break
          num[level] += 1
          for i in range(level+1, len(num)):
            num[i] = 0
          prefix = '.'.join([str(n) for n in num[:level+1] if n>0])
          toc.setdefault(page, []).append(
            f"<span class='toc-line toc-{level}'><span class='prefix-toc'>"+\
            f"{prefix}</span>{b}</span><span class='toc-pagenumber'>"+\
            f"{page}</span>"
          )
          line = f"{a}>{prefix} {b}<{c}"
          break

      buffer.append(line)

      if 'class="page' in line:
        if page == 1:
          continue
        padding = len(line) - len(line.lstrip())
        buffer.append(f'{(padding+2)*" "}<div class="pagenumber"><span>{page}</span></div>')


    return os.linesep.join(buffer), toc

  def citations_resolve(html):
    import bib2json
    references = json.loads(bib2json.read('references.bib'))
    indexes = {}
    index_current = 1
    buffer = []

    def reference_html(word):
      index = indexes[word]
      return f"<span class='citation'>[{index}]</span>"

    def html_references_page():
      references_by_index = {
        index: references[name] for name,index in indexes.items()
      }
      buffer = []
      for index, reference in sorted(references_by_index.items()):
        buffer.append(f"<div><span>{index}: {reference['title']}</span></div>")
      return os.linesep.join(buffer)

    for word in html.split(' '):
      if word.startswith('_cit_'):
        index_trailing = len(word)
        for c in reversed(word):
          if c.isalpha():
            break
          index_trailing -= 1
        word, trailing = word[:index_trailing], word[index_trailing:]
        if word not in indexes:
          indexes[word] = str(index_current)
          index_current += 1
        buffer.append(reference_html(word)+trailing)
      else:
        buffer.append(word)
    html = ' '.join(buffer)
    html = html.replace('!!references!!', html_references_page())
    return html

  def toc_to_html(toc):
    buffer = ['<div id="toc">']
    lvl = 1
    indent = lambda lvl: " "*(2*(lvl+2))
    for page, headings in sorted(toc.items()):
      for heading in headings:
        old_lvl = lvl
        lvl = len(heading.split('.'))+1
        for i in range((old_lvl-lvl)+1):
          buffer.append(f'{indent(old_lvl-(i+1))}  </div>')
        buffer.append(f'{indent(lvl)}<div>')
        buffer.append(f'{indent(lvl+1)}{heading}')
    lvl = 1
    for i in range(old_lvl-lvl):
      buffer.append(f'{indent(old_lvl-i)}  </div>')
    buffer.append('      </div>')
    return os.linesep.join(buffer)

  @app.route('/report')
  def report():
    keywords = [f"keyword{i:02d}" for i in range(5)]
    today = datetime.date.today().strftime("%B %d, %Y")
    html, pdf = render_template(
      "report.html",
      today=today,
      title=title,
      keywords=keywords,
    )
    html = citations_resolve(html)
    html, toc = toc_generate(html)
    html = html.replace('!!toc!!',toc_to_html(toc))
    pdf = save_pdf(html, 'report.pdf')
    return html

  DATABASE2 = 'db2.sqlite3.db'

  @app.teardown_request
  def teardown_request(exception):
    db = g.pop('db2', None)
    if db:
      db.close()

  def _db2():
    if 'db2' in g:
      return g.db2
    g.db2 = sqlite3.connect(DATABASE2)
    g.db2.row_factory = sqlite3.Row
    is_initialized = g.db2.execute(
      "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchone()
    if not is_initialized:
      with open('schema2.sql') as fh:
        g.db2.executescript(fh.read())
      user_ids = set()
      pool = 'abcdefghijklmnopqrstuvwxyz'
      pool += pool.upper()
      pool += '123456789#@!'
      while len(user_ids) < 10e3:
        user_id = ''.join([random.choice(pool) for _ in range(5)])
        user_ids.add(user_id)
      cursor = g.db2.cursor()
      cursor.executemany(
        'INSERT INTO test_user_ids (str_id) VALUES (?)',
        [(user_id,) for user_id in user_ids]
      )
      cursor.close()
      g.db2.commit()

    return g.db2

  @app.route('/webapp/results', methods=['GET'])
  def webapp_results():
    data = _db2().execute(
      "SELECT t_start, t_stop, success FROM test_run"
    ).fetchall()
    html, pdf = render_template(
      'webapp_results.html',
      data=[dict(d) for d in data],
    )
    return html

  @app.route('/webapp/abort', methods=['GET','POST'])
  def abort():

    db = _db2()
    if request.method == "POST":

      id_user = session['id_user']

      if 'btn_abort_delete' in request.form:
        db.execute("DELETE FROM test_user WHERE str_id = (?)", (id_user,))
        db.execute("DELETE FROM test_run WHERE id_user = (?)", (id_user,))
        db.execute("DELETE FROM test_run_vars WHERE id_user = (?)", (id_user,))
        db.execute("DELETE FROM answer WHERE str_id = (?)", (id_user,))
        db.execute(
          "UPDATE test_user_ids SET used=FALSE WHERE str_id = (?)",
          (id_user,)
        )
        db.commit()
        session.clear()

      return redirect(url_for('webapp'))

    html, pdf = render_template(
      'abort.html',
      id_user = session['id_user'],
    )
    return html

  @app.route('/webapp', methods=['GET','POST'])
  def webapp():
    buttons = ['employee hours','team workload','task dependencies','team performance']
    data = ""

    db = _db2()

    def ids_tests_data_types():
      types_from_db = db.execute('SELECT name, id FROM type_data').fetchall()
      return {
        name_type: id_type for name_type, id_type in types_from_db
      }

    def new_run(type_data):
      cursor = db.cursor()
      user = cursor.execute(
        'SELECT * FROM test_user WHERE str_id = (?)',
        (session['id_user'],)
      ).fetchone()
      cursor.execute(
        'INSERT INTO test_run (name, id_user) VALUES (?,?)',
        (type_data, user['str_id'])
      )
      db.commit()
      cursor.close()
      return cursor.lastrowid

    def id_user_get():
      cursor = db.cursor()
      cursor.execute(
        """
        UPDATE test_user_ids SET used=TRUE
        WHERE id=(
          SELECT id FROM test_user_ids WHERE used=FALSE
          ORDER BY id LIMIT 1
        )
        """
      )
      db.commit()
      user_id = cursor.execute(
        """
          SELECT str_id FROM test_user_ids
            WHERE used=1
            ORDER BY id DESC LIMIT 1
        """
      ).fetchone()['str_id']
      cursor.close()
      return user_id

    def db_submit_answers(data_form):
      db = _db2()
      cursor = db.cursor()
      data = [
        (session['id_user'], key, value )
        for key,value in data_form.items() if not key.startswith('btn_')
      ]
      cursor.executemany(
        """
          INSERT INTO answer (str_id, question, answer)
            VALUES (?,?,?)
        """, data
      )
      db.commit()

    def stats_get():
      stats = {
        'num_types': {k:0 for k in buttons},
        'required': 5,
      }
      cursor = db.cursor()
      tasks = cursor.execute(
        "SELECT name FROM test_run WHERE id_user=(?) AND t_stop!= ''",
        (session['id_user'],)
      ).fetchall()
      stats['total'] = len(tasks)
      for task in tasks:
        stats['num_types'][task['name']] += 1
      return stats

    if request.method == 'POST':
      if 'btn_task_type' in request.form:
        session['task_started'] = False
        session['task_type'] = request.form['btn_task_type'].lower()
      elif 'btn_task_start' in request.form:
        session['task_run_id'] = new_run(session['task_type'])
        session['task_started'] = True
      elif 'btn_accept_disclosure' in request.form:
        cursor = db.cursor()
        id_user = id_user_get()
        cursor.execute(
          'INSERT INTO test_user (str_id) VALUES (?);', (id_user,)
        )
        db.commit()
        cursor.close()
        session['accept_disclosure'] = True
        session['id_user'] = id_user
      elif 'btn_survey' in request.form:
        session['survey_take'] = True
      elif 'btn_survey_cancel' in request.form:
        session['survey_take'] = False
      elif 'btn_survey_submit' in request.form:
        db_submit_answers(request.form)
        session.clear()
      elif 'btn_initial_survey' in request.form:
        db_submit_answers(request.form)
        session['survey_initial'] = True
      elif 'not_correct' in request.form:
        cursor = db.cursor()
        now = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%d %H:%M:%f')
        now = now[:-3]
        now += '000UTC'
        cursor.execute(
          'UPDATE test_run SET t_stop = (?), success = (?), answer = (?), answer_correct = (?) WHERE id = (?);',
          (
            now,
            'correct' in request.form,
            request.form.get('answer'),
            request.form.get('answer_correct'),
            session["task_run_id"],
          )
        )
        db.commit()
        cursor.close()
        session['task_started'] = False
        session['task_type'] = ""
      elif 'btn_abort' in request.form:
        return redirect(url_for('abort'))

      return redirect(url_for('webapp'))

    task_run_id = session.get('task_run_id')
    time_start = None
    if task_run_id:
      db_entity = db.execute(
        f'SELECT t_start FROM test_run WHERE id = {task_run_id}'
      ).fetchone()
      if db_entity:
        time_start = datetime.datetime.strptime(
          db_entity[0],
          '%Y-%m-%d %H:%M:%S.%f%Z'
        )

    def data_generate(task_type, seed):
      random.seed(seed)
      data = []
      d = lambda i: data.append(i)

      pallet = [
        "#001f3f",
        "#0074D9",
        "#39CCCC",
        "#3D9970",
        "#2ECC40",
        "#01FF70",
        "#FFDC00",
        "#FF851B",
        "#85144b",
        "#F012BE",
        "#B10DC9"
      ]

      if task_type == 'employee hours':

        num_people = 25
        people = []
        index_correct = random.choice(range(num_people))
        for i in range(num_people):
          available = random.choice(range(45,75)[::10])
          if i == index_correct:
            assigned = 1.3*available
          else:
            assigned = random.uniform(0.5,1.2)*available
          people.append((available, assigned))

        d(f"<form name='form_answer' action='{url_for('webapp')}' method='post'>")
        d("  <input id='checkbox-correct' class='hidden' name='correct' type='checkbox'/>")
        d("  <input id='checkbox-false' class='hidden' name='not_correct' type='checkbox' checked/>")
        d(f" <input id='answer_correct' class='hidden' name='answer_correct' type='text' value='{index_correct}'/>")
        d("  <input id='answer' class='hidden' name='answer' type='text' value=''/>")
        d("  <svg id='svg-data'>")
        d("    <defs>")
        d('      <pattern id="stripe" patternUnits="userSpaceOnUse" width="4" height="4">')
        d('        <path d="M-1,1 l2,-2')
        d('                 M0,4 l4,-4')
        d('                 M3,5 l2,-2" />')
        d('      </pattern>')
        d('      <mask id="mask">')
        d('        <rect height="100%" width="100%" style="fill: url(#stripe)" />')
        d('      </mask>')
        d("    </defs>")
#        d("    <style> rect { cursor: pointer; } rect:hover { fill: lightgrey } </style>")
        offset = 0
        y_end = 95
        increment = 90/num_people
        random.shuffle(pallet)
        color = pallet.pop(0)
        color_overshot = pallet.pop(0)
        width = 3
        for i, (available, assigned) in enumerate(people):
          command = f"document.getElementById('answer').value='{index_correct}';document.form_answer.submit()"
          if i == index_correct:
            command = f"document.getElementById('checkbox-correct').checked = true;{command}"
          if assigned > available:
            d(f'<rect class="clickable" x="{5+offset}%" y="{y_end-assigned}%" width="{width}%" height="{assigned-available}%" fill="{color_overshot}" stroke="black" onclick="{command}"/>')
            d(f'<rect x="{5+offset}%" y="{y_end-available}%" width="{width}%" height="{available}%" stroke="black" fill="{color}" />')
          else:
            d(f'<rect x="{5+offset}%" y="{y_end-assigned}%" width="{width}%" height="{assigned}%" fill="{color}" stroke="black"/>')
            d(f'<rect x="{5+offset}%" y="{y_end-available}%" width="{width}%" height="{available-assigned}%" stroke="black" fill="none"/>')
          offset += increment
        d("    <text class='legendx' x='50%' y='96.5%'>Assignment ratio per employee</text>")
        d("    <text class='legend_title' x='50%' y='3%'>Employee Hours</text>")
        d("    <text class='legendy' x='-2.5%' y='-50%'>Assigned vs. Available Hours</text>")
        d("  </svg>")
        d("</form>")
        vars = ';'.join([
          f'{num_people=}',
          f'{color=}',
          f'{color_overshot=}',
          f'{people=}',
        ])

      elif task_type == 'team workload':

        d(f"<form name='form_answer' action='{url_for('webapp')}' method='post'>")
        d("  <input id='checkbox-correct' class='hidden' name='correct' type='checkbox'/>")
        d("  <input id='checkbox-false' class='hidden' name='not_correct' type='checkbox' checked/>")
        d("  <input id='answer' class='hidden' name='answer' type='text' value=''/>")
        color = random.choice(pallet)
        num_x = 5
        num_y = 25
        num = num_x * num_y
        opacities = [random.uniform(0.1,0.5) for _ in range(int(0.7*num))]
        opacities += [random.uniform(0.5,0.6) for _ in range(int(0.2*num))]
        opacities += [random.uniform(0.6,0.80) for _ in range(int(0.1*num))]
        opacities += [0.0]*(num-len(opacities))
        opacities.pop()
        opacities.append(1.0)
        opacities_copy = list(opacities)
        random.shuffle(opacities)
        offset_x = 8
        offset_y = 15
        workable_x = 100-offset_x
        workable_y = 100-offset_y
        width = workable_x/(num_x)
        height = workable_y/(num_y)
        days = "MON TUE WED THU FRI".split()
        d("  <svg id='svg-data'>")
        d("    <style> rect { cursor: pointer; } rect:hover { fill: lightgrey; }</style>")
        for y in range(num_y):
          for x in range(num_x):
            opacity = opacities[x + y*num_x]
            command = f"document.getElementById('answer').value = '({x},{y})';document.form_answer.submit()"
            if opacity == 1.0:
              data.insert(3, f"  <input id='answer_correct' class='hidden' name='answer_correct' type='text' value='({x},{y})'/>")
              command = f"document.getElementById('checkbox-correct').checked = true;{command}"
            d(f"<rect x='{offset_x/2+x*width}%' y='{offset_y/2+y*height}%' width='{width}%' height='{height}%' fill='{color}' stroke='black' stroke-width='0.3' style='fill-opacity: {opacity};' onclick=\"{command}\"/>")
        for i, y in enumerate(range(num_y), start=1):
          d(f"<text x='{offset_x/2}%' y='{offset_y/2+y*height+height/1.5}%'>W{i:02d}</text>")
        for i, x in enumerate(range(num_x), start=0):
          d(f"<text x='{offset_x/2+x*width+width/2.5}%' y='7%'>{days[i]}</text>")
        d("    <text class='legend_title' x='50%' y='3%'>Team Workload</text>")
        d("    <text class='legendy' x='-2.0%' y='-50%'>Work Week</text>")
        d("  </svg>")
        d("</form>")
        vars = ';'.join([
          f'{color=}',
          f'{opacities=}',
        ])

      elif task_type == 'task dependencies':

        dot_width = 3.3
        num_dots = 17
        dot_angle = 2*math.pi / num_dots
        dots = []
        max_connections = 3
        connections_correct_additional = 3
        index_correct = random.choice(range(num_dots))

        radius = 38
        for i in range(num_dots):
          x = 50 + radius * math.cos(dot_angle*i + math.pi)
          y = 50 + radius * math.sin(dot_angle*i + math.pi)
          if i == index_correct:
            connections = max_connections + connections_correct_additional
          else:
            connections = random.randrange(1,max_connections)
          dots.append((i,x,y,connections))

        d(f"<form name='form_answer' action='{url_for('webapp')}' method='post'>")
        d("  <input id='checkbox-correct' class='hidden' name='correct' type='checkbox'/>")
        d("  <input id='checkbox-false' class='hidden' name='not_correct' type='checkbox' checked/>")
        d("  <input id='answer' class='hidden' name='answer' type='text' value=''/>")
        d("  <svg id='svg-data'>")
#        d("    <style> circle { cursor: pointer; } circle:hover { fill: lightgrey; } .tag:hover { color: blue; }</style>")
        connections_all = [[0]*num_dots for _ in range(num_dots)]
        for dot in dots:
          index,x,y,connections = dot
          others = dots[:index] + dots[index:]
          random.shuffle(others)
          color = random.choice(pallet)
          while sum(connections_all[index]) < connections:
            dot_connections = connections_all[index]
            while True:
              connect_to = random.choice(range(len(dot_connections)))
              if sum(connections_all[connect_to]) < max_connections:
                connections_all[connect_to][index] = 1
                connections_all[index][connect_to] = 1
                break

        set_connections = set()
        color = random.choice(pallet)
        for i, conns in enumerate(connections_all):
          for ii, con in enumerate(conns):
            if con == 0:
              continue
            if (i, ii) in set_connections or (ii, i) in set_connections:
              continue
            set_connections.add((i, ii))
            _, x, y, _ = dots[i]
            _, ox, oy, _ = dots[ii]
            d(f"<line x1='{x}%' x2='{ox}%' y1='{y}%' y2='{oy}%' stroke='{color}' stroke-width='0.3%' stroke-opacity='0.5'/>")
        for dot in dots:
          command = f"document.getElementById('answer').value = '{index}';document.form_answer.submit()"
          index,x,y,_ = dot
          if index == index_correct:
            command = f"document.getElementById('checkbox-correct').checked = true;{command}"
          d(f"<g class='group_circle'>")
          d(f"  <circle cx='{x}%' cy='{y}%' r={dot_width}% fill='#eee' stroke='#555' stroke-width='0.3%' onclick=\"{command}\"/>")
          d(f"  <text x='{x}%' y='{y}%'>T{index:02d}</text>")
          d(f"</g>")
        d("    <text class='legend_title' x='50%' y='3%' fill='black' >Task Dependencies</text>")
        d("  </svg>")
        d("</form>")
        vars = ';'.join([str(v) for v in [
          f'{color=}',
          f'{index_correct=}',
          f'{connections_all=}',
        ]])

      elif task_type == 'team performance':

        #pallet = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
        #pallet = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
        tasks = ["tickets","rnd","support","features","maintenance"]


        random.shuffle(pallet)

        colors = { k:v for k,v in zip(tasks, pallet) }

        #http://www.perceptualedge.com/articles/visual_business_intelligence/rules_for_using_color.pdf

        num_teams = random.randrange(7,10)
        spacing_vertical = 80/num_teams
        teams = []

        index_correct = random.choice(range(num_teams))

        spread_max = 0
        spread_sum_max = 0
        def get_spread(i):
          index_rect_max = 0
          nonlocal spread_max, spread_sum_max
          spread = []
          if i == index_correct:
            num_tasks = 1050
          else:
            num_tasks = random.randint(700,1000)
          top = int(num_tasks * 0.3)
          num_tasks -= top
          spread.append(top)
          for _ in range(len(tasks)-2):
            pick_tasks = int(num_tasks * random.uniform(0.3,0.4))
            num_tasks -= pick_tasks
            spread.append(pick_tasks)
          spread.append(num_tasks)
          random.shuffle(spread)

          spread_sum = sum(spread)
          spread_max = max(spread_max, max(spread))
          if spread_sum > spread_sum_max:
            index_rect_max = spread.index(top)
            spread_sum_max = spread_sum
          spread_sum = sum(spread)

          return (index_rect_max, list(zip(tasks, spread)), spread_sum)

        spreads = [get_spread(i) for i in range(num_teams)]

        for i in range(num_teams):
          teams.append((0,i*spacing_vertical,*spreads[i]))

        d(f"<form name='form_answer' action='{url_for('webapp')}' method='post'>")
        d("  <input id='checkbox-false' class='hidden' name='not_correct' type='checkbox' checked/>")
        d("  <input id='checkbox-correct' name='correct' type='checkbox'/>")
        d("  <input id='answer' class='hidden' name='answer' type='text' value=''/>")
        d("  <svg id='svg-data'>")
#        d("    <style> rect { cursor: pointer; } rect:hover { fill: lightgrey; } </style>")
        offset_y = 8
        for i,team in enumerate(teams):
          x,y,index_max,parts,parts_sum = team
          offset = 0
          for ii, (name, p)  in enumerate(parts):
            command = f"document.getElementById('answer').value='({i},{ii})';document.form_answer.submit()"
            if i == index_correct and ii == index_max:
              command = f"document.getElementById('checkbox-correct').checked = true;{command}"
            color = colors[name]
            p = (90*p/parts_sum)*(parts_sum/spread_sum_max)
            d('<g class="group_performance">')
            d(f'  <rect class="part_performance" x="{5+x+offset}%" y="{offset_y+y}%" width="{p}%" height="5%" fill="{color}" stroke="black" stroke-width="2.0" onclick="{command}"/>')
            if p < len(name)+2:
              name = name[:3]+'..'
            d(f'  <text class="text_performance" x="{5+x+offset+p/2}%" y="{offset_y+y+2.5}%" fill="black">{name.title()}</text>')
            if ii == 0:
              d(f'  <text x="{5+x+offset}%" y="{offset_y+y-0.5}%" fill="black">Team {i+1:02d}</text>')
            d('</g>')
            offset += p
        d("    <text class='legend_title' x='50%' y='3%' fill='black' >Team Performance</text>")
        d("  </svg>")
        d("</form>")
        vars = ';'.join([
          f'{index_max=}',
          f'{index_correct=}',
          f'{teams=}',
        ])

      vars += ';'+f'{data=}'
      cursor = db.cursor()
      cursor.execute(
        "INSERT INTO test_run_vars (id_test_run, id_user, vars) VALUES (?,?,?)",
        (seed, session['id_user'], vars)
      )
      db.commit()
      cursor.close()
      return os.linesep.join(data)

    task_type = session.get('task_type')
    task_started = session.get('task_started')
    accept_disclosure = session.get('accept_disclosure')

    description = {
      'employee hours': """
        <strong>Goal:</strong> <br>
        Select the most over-booked employee.
        <br>
        <br>
        <strong>How:</strong> <br>
        This task present a bar-chart (one bar per employee) <br>
        where the bar represents their available time. <br>
        <br>
        If their work-load is lower than the total available hours <br>
        the bar will be partially filled, showing the white background. <br>
        <br>
        If the planned work-load exceeds the total amount of available <br>
        hour the fill will go beyond the bar and turn a different color. <br>
        <br>
        Click the largest other-colored section in order to <br>
        select the most over-booked employee.
      """,
      'team workload': """
        <strong>Goal:</strong> <br>
        Select the busiest day in the calendar.
        <br>
        <br>
        <strong>How:</strong> <br>
        This task present a colored grid where each cell represents a day of <br>
        a 5-day work week. The more intense the color, the more things <br>
        are scheduled to be done at that day. <br>
        <br>
        Click the most color-intense cell in order to select the busiest day.
      """,
      'task dependencies': """
        <strong>Goal:</strong><br>
        Select the task with the most connections.
        <br>
        <br>
        <strong>How:</strong> <br>
        This task present several circles representing tasks. <br>
        <br>
        The connected lines represent how many dependencies are linked <br>
        to that task. More lines -> more dependencies. <br>
        <br>
        Click the circle with the most lines attached to it.
      """,
      'team performance': """
        <strong>Goal:</strong><br>
        Select the area where the most performant team did the most work.
        <br>
        <br>
        <strong>How:</strong> <br>
        This task present several horizontal bars representing the total <br>
        work of different teams. Longer bar -> more work done. <br>
        <br>
        The bars are then divided into differently colored and labeled <br>
        sections. These sections represent different type of work done by<br>
        the team. Same thing here, larger section -> more done. <br>
        <br>
        First find the team that did the most work (longest bar) then click <br>
        the largest sub-section of that bar.
      """,
    }

    if not accept_disclosure:
      html, pdf = render_template(
        'disclosure.html',
      )
      return html
    elif task_type:
      if not task_started:
        data = f"""
          <div id='description'>
            <h2>{task_type.title()}</h2>
            {description.get(task_type, "")}
          <div>
        """
      else:
        data = data_generate(task_type, task_run_id);
    else:
      data = ""

    stats = stats_get()


    if session.get('survey_take'):

      questions = [
        "The goal of each task was clear",
        "Test-application looks good",
        "Use of colors helped with the tasks",
        "Amount of information was adequate",
        "Test-application is easy to to navigate",
        "Appropriate choice of colors",
        "Language used was easy to understand",
        "Easy to understand what to do next",
      ]

      if not session.get('survey_done'):
        html, pdf = render_template(
          'survey.html',
          questions=questions,
        )
        return html
      else:
        session['survey_take'] = False

    html, pdf = render_template(
      'webapp.html',
      buttons=buttons,
      data=data,
      task_type=task_type,
      task_started=task_started,
      stats=stats,
    )
    return html

  return app
