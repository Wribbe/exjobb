#!/usr/bin/env python3

import os
import sys
import sqlite3

from exjobb.webapp import webapp

app = webapp.create_app()
os.environ["FLASK_ENV"] = "development"
os.environ["FLASK_DEBUG"] = "True"

def init_db():
  from exjobb.webapp.webapp import DATABASE
  db = sqlite3.connect(DATABASE)
  with open('schema.sql', mode='r') as f:
    db.cursor().executescript(f.read())
    db.commit()
  db.close()

if __name__ == "__main__":
  if '--init' in sys.argv[1:]:
    init_db()
  else:
    app.run(host="0.0.0.0", port=8000)
