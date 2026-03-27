-- =============================================
-- Удаление старых таблиц
-- =============================================
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Manufacturers;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS OrderStatuses;

-- =============================================
-- Создание таблиц
-- =============================================
CREATE TABLE Roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200)
);

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES Roles(id)
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE Manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100),
    website VARCHAR(200)
);

CREATE TABLE Suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article VARCHAR(50) UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER,
    manufacturer_id INTEGER,
    supplier_id INTEGER,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    unit VARCHAR(20) DEFAULT 'шт',
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    discount INTEGER DEFAULT 0 CHECK (discount >= 0 AND discount <= 100),
    image_path VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(id),
    FOREIGN KEY (manufacturer_id) REFERENCES Manufacturers(id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(id)
);

CREATE TABLE OrderStatuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(50) UNIQUE,
    user_id INTEGER,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATETIME,
    pickup_point VARCHAR(300),
    status_id INTEGER,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (status_id) REFERENCES OrderStatuses(id)
);

CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order DECIMAL(10,2) NOT NULL,
    discount_at_order INTEGER DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(id)
);

-- =============================================
-- Базовые справочные данные
-- =============================================
INSERT INTO Roles (id, name, description) VALUES 
    (1, 'Администратор', 'Администратор - полный доступ'),
    (2, 'Менеджер', 'Менеджер - управление товарами и просмотр заказов'),
    (3, 'Авторизированный клиент', 'Клиент - просмотр товаров');

INSERT INTO OrderStatuses (id, name, description) VALUES 
    (1, 'Новый', 'Заказ создан, ожидает обработки'),
    (2, 'В обработке', 'Заказ обрабатывается'),
    (3, 'Готов к выдаче', 'Заказ готов, можно забирать'),
    (4, 'Выдан', 'Заказ выдан клиенту'),
    (5, 'Отменен', 'Заказ отменен'),
    (6, 'Завершен', 'Заказ выполнен');

INSERT OR IGNORE INTO Suppliers (name) VALUES 
    ('Kari'),
    ('Обувь для вас');

INSERT OR IGNORE INTO Manufacturers (name) VALUES 
    ('Kari'),
    ('Marco Tozzi'),
    ('Рос'),
    ('Rieker'),
    ('Alessio Nesca'),
    ('CROSBY');

INSERT OR IGNORE INTO Categories (name) VALUES 
    ('Женская обувь'),
    ('Мужская обувь');

-- =============================================
-- Создание индексов
-- =============================================
CREATE INDEX idx_products_name ON Products(name);
CREATE INDEX idx_products_article ON Products(article);
CREATE INDEX idx_products_category ON Products(category_id);
CREATE INDEX idx_products_manufacturer ON Products(manufacturer_id);
CREATE INDEX idx_products_supplier ON Products(supplier_id);
CREATE INDEX idx_orders_user ON Orders(user_id);
CREATE INDEX idx_orders_status ON Orders(status_id);
CREATE INDEX idx_orderitems_order ON OrderItems(order_id);
CREATE INDEX idx_orderitems_product ON OrderItems(product_id);
