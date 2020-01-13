CREATE TABLE test_user_ids (
  id INTEGER PRIMARY KEY
  ,str_id TEXT NOT NULL
  ,used BOOLEAN DEFAULT FALSE
);

CREATE TABLE test_user (
  id INTEGER PRIMARY KEY
  ,t_created TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f000UTC', 'NOW'))
  ,str_id TEXT NOT NULL UNIQUE
);

CREATE TABLE test_run (
  id INTEGER PRIMARY KEY
  ,name TEXT NOT NULL
  ,id_user TEXT NOT NULL
  ,t_start TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f000UTC', 'NOW'))
  ,t_stop TEXT DEFAULT ""
  ,answer TEXT DEFAULT ""
  ,answer_correct TEXT DEFAULT ""
  ,success BOOLEAN DEFAULT FALSE
  ,vars TEXT
  ,FOREIGN KEY(id_user) REFERENCES test_user(str_id)
);

CREATE TABLE answer (
  id INTEGER PRIMARY KEY
  ,str_id TEXT NOT NULL
  ,question TEXT NOT NULL
  ,answer TEXT NOT NULL
  ,FOREIGN KEY(str_id) REFERENCES test_user(str_id)
);
