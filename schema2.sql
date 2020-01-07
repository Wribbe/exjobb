CREATE TABLE test_user_ids (
  id INTEGER PRIMARY KEY
  ,str_id TEXT NOT NULL
  ,used BOOLEAN DEFAULT FALSE
);

CREATE TABLE test_user (
  id INTEGER PRIMARY KEY
  ,t_created TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f000UTC', 'NOW'))
  ,str_id TEXT NOT NULL
);

CREATE TABLE test_run (
  id INTEGER PRIMARY KEY
  ,name TEXT NOT NULL
  ,id_user INTEGER NOT NULL
  ,t_start TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f000UTC', 'NOW'))
  ,t_stop TEXT DEFAULT ""
  ,answer TEXT DEFAULT ""
  ,answer_correct TEXT DEFAULT ""
  ,success BOOLEAN DEFAULT FALSE
  ,vars TEXT
  ,FOREIGN KEY(id_user) REFERENCES test_user(id)
);
