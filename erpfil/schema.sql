-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS partner_type;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS deal;
DR

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE
);

CREATE TABLE product_unit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL UNIQUE
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  category_id INTEGER,
  article INTEGER UNIQUE,
  unit_id INTEGER,
  comment TEXT,
  FOREIGN KEY (category_id) REFERENCES product_category (id),
  FOREIGN KEY (unit_id) REFERENCES product_unit (id)
);

CREATE TABLE partner_type (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT UNIQUE NOT NULL,
  customer INTEGER NOT NULL,
  contractor INTEGER NOT NULL
);

CREATE TABLE partner (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  full_name TEXT,
  phone TEXT,
  phone_1 TEXT,
  website TEXT,
  contact_person TEXT,
  address TEXT,
  note TEXT,
  manager_id INTEGER NOT NULL,
  partner_type_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (manager_id) REFERENCES user (id),
  FOREIGN KEY (partner_type_id) REFERENCES partner_type (id)
);

CREATE TABLE deal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  number INTEGER NOT NULL AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_expected TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  customer_id INTEGER NOT NULL,
  invoice_no TEXT,
  tz_no TEXT,
  payment_order_no TEXT,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  manager_id INTEGER NOT NULL,
  FOREIGN KEY (manager_id) REFERENCES user (id),
  FOREIGN KEY (customer_id) REFERENCES partner (id)
);

-- Contractors for each deal (connection table)
CREATE TABLE deal_product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  deal_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  product_customer_quantity INTEGER NOT NULL,
  product_supplier_quantity INTEGER NOT NULL,
  product_customer_price REAL NOT NULL,
  product_supplier_price REAL NOT NULL,
  contractor_id INTEGER NOT NULL,
  FOREIGN KEY (deal_id) REFERENCES deal (id),
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (contractor_id) REFERENCES partner (id)
);


