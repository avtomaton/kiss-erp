-- Fill the database with initial values.

DELETE FROM partner_type;
INSERT INTO partner_type (title, customer, contractor) VALUES(
  "Клиент", 1, 0
);
INSERT INTO partner_type (title, customer, contractor) VALUES(
  "Подрядчик", 0, 1
);
INSERT INTO partner_type (title, customer, contractor) VALUES(
  "Поставщик", 0, 1
);
INSERT INTO partner_type (title, customer, contractor) VALUES(
  "Клиент/Подрядчик", 1, 1
);
INSERT INTO partner_type (title, customer, contractor) VALUES(
  "Сервис", 0, 1
);
