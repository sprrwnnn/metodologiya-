-- =============================================
-- Импорт пользователей из user_import.xlsx
-- =============================================
INSERT OR IGNORE INTO Users (login, password, full_name, role_id) VALUES 
    ('94d5ous@gmail.com', 'uzWC67', 'Никифорова Весения Николаевна', 1),
    ('uth4iz@mail.com', '2L6KZG', 'Сазонов Руслан Германович', 1),
    ('yzls62@outlook.com', 'JlFRCZ', 'Одинцов Серафим Артёмович', 1),
    ('1diph5e@tutanota.com', '8ntwUp', 'Степанов Михаил Артёмович', 2),
    ('tjde7c@yahoo.com', 'YOyhfR', 'Ворсин Петр Евгеньевич', 2),
    ('wpmrc3do@tutanota.com', 'RSbvHv', 'Старикова Елена Павловна', 2),
    ('5d4zbu@tutanota.com', 'rwVDh9', 'Михайлюк Анна Вячеславовна', 3),
    ('ptec8ym@yahoo.com', 'LdNyos', 'Ситдикова Елена Анатольевна', 3),
    ('1qz4kw@mail.com', 'gynQMT', 'Ворсин Петр Евгеньевич', 3),
    ('4np6se@mail.com', 'AtnDjr', 'Старикова Елена Павловна', 3);

-- =============================================
-- Импорт товаров из Tovar.xlsx (первые 12)
-- =============================================
INSERT INTO Products (article, name, unit, price, supplier_id, manufacturer_id, category_id, discount, quantity, description, image_path) VALUES 
    ('А112Т4', 'Ботинки', 'шт', 4990, 
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Kari'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 3, 6, 'Женские Ботинки демисезонные kari', '1.jpg'),
    ('F635R4', 'Ботинки', 'шт', 3244,
        (SELECT id FROM Suppliers WHERE name='Обувь для вас'),
        (SELECT id FROM Manufacturers WHERE name='Marco Tozzi'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 2, 13, 'Ботинки Marco Tozzi женские', '2.jpg'),
    ('H782T5', 'Туфли', 'шт', 4499,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Kari'),
        (SELECT id FROM Categories WHERE name='Мужская обувь'), 4, 5, 'Туфли kari мужские классика', '3.jpg'),
    ('G783F5', 'Ботинки', 'шт', 5900,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Рос'),
        (SELECT id FROM Categories WHERE name='Мужская обувь'), 2, 8, 'Мужские ботинки Рос-Обувь', '4.jpg'),
    ('J384T6', 'Ботинки', 'шт', 3800,
        (SELECT id FROM Suppliers WHERE name='Обувь для вас'),
        (SELECT id FROM Manufacturers WHERE name='Rieker'),
        (SELECT id FROM Categories WHERE name='Мужская обувь'), 2, 16, 'Полуботинки мужские Rieker', '5.jpg'),
    ('D572U8', 'Кроссовки', 'шт', 4100,
        (SELECT id FROM Suppliers WHERE name='Обувь для вас'),
        (SELECT id FROM Manufacturers WHERE name='Рос'),
        (SELECT id FROM Categories WHERE name='Мужская обувь'), 3, 6, 'Кроссовки мужские', '6.jpg'),
    ('F572H7', 'Туфли', 'шт', 2700,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Marco Tozzi'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 2, 14, 'Туфли Marco Tozzi женские', '7.jpg'),
    ('D329H3', 'Полуботинки', 'шт', 1890,
        (SELECT id FROM Suppliers WHERE name='Обувь для вас'),
        (SELECT id FROM Manufacturers WHERE name='Alessio Nesca'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 4, 4, 'Полуботинки Alessio Nesca', '8.jpg'),
    ('B320R5', 'Туфли', 'шт', 4300,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Rieker'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 2, 6, 'Туфли Rieker женские', '9.jpg'),
    ('G432E4', 'Туфли', 'шт', 2800,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Kari'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 3, 15, 'Туфли kari женские', '10.jpg'),
    ('S213E3', 'Полуботинки', 'шт', 2156,
        (SELECT id FROM Suppliers WHERE name='Обувь для вас'),
        (SELECT id FROM Manufacturers WHERE name='CROSBY'),
        (SELECT id FROM Categories WHERE name='Мужская обувь'), 3, 6, 'Полуботинки мужские CROSBY', NULL),
    ('E482R4', 'Полуботинки', 'шт', 1800,
        (SELECT id FROM Suppliers WHERE name='Kari'),
        (SELECT id FROM Manufacturers WHERE name='Kari'),
        (SELECT id FROM Categories WHERE name='Женская обувь'), 2, 14, 'Полуботинки kari женские', NULL);

-- =============================================
-- Импорт заказов
-- =============================================
DELETE FROM OrderItems;
DELETE FROM Orders;

INSERT INTO Orders (order_number, order_date, delivery_date, pickup_point, user_id, status_id) VALUES 
    ('1', '2025-02-27 00:00:00', '2025-04-20 00:00:00', '420151, г. Лесной, ул. Вишневая, 32', 
        (SELECT id FROM Users WHERE full_name='Степанов Михаил Артёмович'), 6),
    ('2', '2022-09-28 00:00:00', '2025-04-21 00:00:00', '410172, г. Лесной, ул. Северная, 13',
        (SELECT id FROM Users WHERE full_name='Никифорова Весения Николаевна'), 6),
    ('3', '2025-03-21 00:00:00', '2025-04-22 00:00:00', '630370, г. Лесной, ул. Шоссейная, 24',
        (SELECT id FROM Users WHERE full_name='Сазонов Руслан Германович'), 6),
    ('4', '2025-02-20 00:00:00', '2025-04-23 00:00:00', '410172, г. Лесной, ул. Северная, 13',
        (SELECT id FROM Users WHERE full_name='Одинцов Серафим Артёмович'), 6),
    ('5', '2025-03-17 00:00:00', '2025-04-24 00:00:00', '630370, г. Лесной, ул. Шоссейная, 24',
        (SELECT id FROM Users WHERE full_name='Степанов Михаил Артёмович'), 6),
    ('6', '2025-03-01 00:00:00', '2025-04-25 00:00:00', '603036, г. Лесной, ул. Садовая, 4',
        (SELECT id FROM Users WHERE full_name='Никифорова Весения Николаевна'), 6),
    ('7', '2025-02-28', '2025-04-26 00:00:00', '454311, г.Лесной, ул. Новая, 19',
        (SELECT id FROM Users WHERE full_name='Сазонов Руслан Германович'), 6),
    ('8', '2025-03-31 00:00:00', '2025-04-27 00:00:00', '625683, г. Лесной, ул. 8 Марта',
        (SELECT id FROM Users WHERE full_name='Одинцов Серафим Артёмович'), 1),
    ('9', '2025-04-02 00:00:00', '2025-04-28 00:00:00', '614510, г. Лесной, ул. Маяковского, 47',
        (SELECT id FROM Users WHERE full_name='Степанов Михаил Артёмович'), 1),
    ('10', '2025-04-03 00:00:00', '2025-04-29 00:00:00', '625683, г. Лесной, ул. 8 Марта',
        (SELECT id FROM Users WHERE full_name='Степанов Михаил Артёмович'), 1);

-- =============================================
-- Импорт элементов заказов
-- =============================================
INSERT INTO OrderItems (order_id, product_id, quantity, price_at_order) VALUES 
    (1, (SELECT id FROM Products WHERE article='А112Т4'), 2, 4990),
    (1, (SELECT id FROM Products WHERE article='F635R4'), 2, 3244),
    (2, (SELECT id FROM Products WHERE article='H782T5'), 1, 4499),
    (2, (SELECT id FROM Products WHERE article='G783F5'), 1, 5900),
    (3, (SELECT id FROM Products WHERE article='J384T6'), 10, 3800),
    (3, (SELECT id FROM Products WHERE article='D572U8'), 10, 4100),
    (4, (SELECT id FROM Products WHERE article='F572H7'), 5, 2700),
    (4, (SELECT id FROM Products WHERE article='D329H3'), 4, 1890),
    (5, (SELECT id FROM Products WHERE article='А112Т4'), 2, 4990),
    (5, (SELECT id FROM Products WHERE article='F635R4'), 2, 3244),
    (6, (SELECT id FROM Products WHERE article='H782T5'), 1, 4499),
    (6, (SELECT id FROM Products WHERE article='G783F5'), 1, 5900),
    (7, (SELECT id FROM Products WHERE article='J384T6'), 10, 3800),
    (7, (SELECT id FROM Products WHERE article='D572U8'), 10, 4100),
    (8, (SELECT id FROM Products WHERE article='F572H7'), 5, 2700),
    (8, (SELECT id FROM Products WHERE article='D329H3'), 4, 1890),
    (9, (SELECT id FROM Products WHERE article='B320R5'), 5, 4300),
    (9, (SELECT id FROM Products WHERE article='G432E4'), 1, 2800),
    (10, (SELECT id FROM Products WHERE article='S213E3'), 5, 2156),
    (10, (SELECT id FROM Products WHERE article='E482R4'), 5, 1800);

-- =============================================
-- Обновление общей суммы заказов
-- =============================================
UPDATE Orders SET total_amount = (
    SELECT SUM(quantity * price_at_order) 
    FROM OrderItems 
    WHERE OrderItems.order_id = Orders.id
);
