-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS deal;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  full_name TEXT,
  phone TEXT,
  website TEXT,
  contact_person TEXT,
  address TEXT,
  note TEXT,
  manager_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (manager_id) REFERENCES user (id)
);

CREATE TABLE deal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  manager_id INTEGER NOT NULL,
  customer_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (manager_id) REFERENCES user (id),
  FOREIGN KEY (customer_id) REFERENCES customer (id)
);
