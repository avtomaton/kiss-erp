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

DELETE FROM product_unit;
INSERT INTO product_unit (title) VALUES('м2');
INSERT INTO product_unit (title) VALUES('м3');
INSERT INTO product_unit (title) VALUES('упак.');
INSERT INTO product_unit (title) VALUES('шт.');

DELETE FROM partner;
INSERT INTO partner (title, partner_type_id, manager_id) VALUES(
  'РАНХИГС', 1, 1
);
INSERT INTO partner (title, partner_type_id, manager_id) VALUES(
  'ООО "Дело Жизни"', 1, 1
);
INSERT INTO partner (title, partner_type_id, manager_id) VALUES(
  'ООО "Принт-маркет"', 3, 1
);
INSERT INTO partner (title, partner_type_id, manager_id) VALUES(
  'ООО "Премьер-Видео"', 3, 1
);
