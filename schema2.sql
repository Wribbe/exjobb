CREATE TABLE type_data (
  id INTEGER PRIMARY KEY
  ,name TEXT NOT NULL
);

CREATE TABLE test_run (
  id INTEGER PRIMARY KEY
  ,t_start TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))
  ,id_type_data INTEGER NOT NULL
  ,FOREIGN KEY (id_type_data) REFERENCES type_data (id)
);
