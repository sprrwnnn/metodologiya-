import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import os


class DatabaseManager:
    """Класс для управления подключением к базе данных"""

    def __init__(self, db_path: str = "shoe_store.db"):
        self.db_path = db_path

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для работы с БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Выполнение SELECT запроса"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Выполнение UPDATE/INSERT/DELETE запроса"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid

    def get_user_by_credentials(self, login: str, password: str) -> Optional[Dict]:
        """Получение пользователя по логину и паролю"""
        query = """
            SELECT u.*, r.name as role_name 
            FROM Users u
            JOIN Roles r ON u.role_id = r.id
            WHERE u.login = ? AND u.password = ?
        """
        result = self.execute_query(query, (login, password))
        return result[0] if result else None

    def get_all_products(self) -> List[Dict]:
        """Получение всех товаров"""
        query = """
            SELECT p.*, 
                   c.name as category_name,
                   m.name as manufacturer_name,
                   s.name as supplier_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Manufacturers m ON p.manufacturer_id = m.id
            LEFT JOIN Suppliers s ON p.supplier_id = s.id
            ORDER BY p.name
        """
        return self.execute_query(query)

    def get_all_products_filtered(
        self,
        search: str = "",
        supplier_filter: str = "",
        sort_by: str = "name",
        sort_order: str = "ASC",
    ) -> List[Dict]:
        """
        Получение списка товаров с фильтрацией, поиском и сортировкой
        search - поисковый запрос (поиск по названию, артикулу, описанию)
        supplier_filter - фильтр по поставщику
        sort_by - поле для сортировки (name, price, quantity, discount)
        sort_order - направление сортировки (ASC, DESC)
        """
        query = """
            SELECT p.*, 
                   c.name as category_name,
                   m.name as manufacturer_name,
                   s.name as supplier_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Manufacturers m ON p.manufacturer_id = m.id
            LEFT JOIN Suppliers s ON p.supplier_id = s.id
            WHERE 1=1
        """
        params = []

        # Поиск по текстовым полям
        if search:
            query += """ AND (
                p.name LIKE ? OR 
                p.article LIKE ? OR 
                p.description LIKE ? OR
                c.name LIKE ? OR
                m.name LIKE ? OR
                s.name LIKE ?
            )"""
            search_param = f"%{search}%"
            params.extend(
                [
                    search_param,
                    search_param,
                    search_param,
                    search_param,
                    search_param,
                    search_param,
                ]
            )

        # Фильтр по поставщику
        if supplier_filter and supplier_filter != "Все поставщики":
            query += " AND s.name = ?"
            params.append(supplier_filter)

        # Сортировка (с защитой от SQL инъекций)
        allowed_columns = ["name", "price", "quantity", "discount"]
        allowed_orders = ["ASC", "DESC"]

        if sort_by not in allowed_columns:
            sort_by = "name"
        if sort_order.upper() not in allowed_orders:
            sort_order = "ASC"

        query += f" ORDER BY {sort_by} {sort_order}"

        return self.execute_query(query, tuple(params))

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Получение товара по ID"""
        query = """
            SELECT p.*, 
                   c.name as category_name,
                   m.name as manufacturer_name,
                   s.name as supplier_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.id
            LEFT JOIN Manufacturers m ON p.manufacturer_id = m.id
            LEFT JOIN Suppliers s ON p.supplier_id = s.id
            WHERE p.id = ?
        """
        result = self.execute_query(query, (product_id,))
        return result[0] if result else None

    def get_suppliers_list(self) -> List[str]:
        """Получение списка всех поставщиков для фильтра"""
        query = "SELECT DISTINCT name FROM Suppliers ORDER BY name"
        result = self.execute_query(query)
        return [row["name"] for row in result]

    def add_product(self, product_data: Dict) -> int:
        """Добавление нового товара"""
        query = """
            INSERT INTO Products 
            (article, name, description, category_id, manufacturer_id, 
             supplier_id, price, unit, quantity, discount, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            product_data.get("article"),
            product_data.get("name"),
            product_data.get("description"),
            product_data.get("category_id"),
            product_data.get("manufacturer_id"),
            product_data.get("supplier_id"),
            product_data.get("price"),
            product_data.get("unit"),
            product_data.get("quantity"),
            product_data.get("discount"),
            product_data.get("image_path"),
        )
        return self.execute_update(query, params)

    def update_product(self, product_id: int, product_data: Dict):
        """Обновление товара"""
        query = """
            UPDATE Products 
            SET article=?, name=?, description=?, category_id=?, 
                manufacturer_id=?, supplier_id=?, price=?, unit=?, 
                quantity=?, discount=?, image_path=?
            WHERE id=?
        """
        params = (
            product_data.get("article"),
            product_data.get("name"),
            product_data.get("description"),
            product_data.get("category_id"),
            product_data.get("manufacturer_id"),
            product_data.get("supplier_id"),
            product_data.get("price"),
            product_data.get("unit"),
            product_data.get("quantity"),
            product_data.get("discount"),
            product_data.get("image_path"),
            product_id,
        )
        self.execute_update(query, params)

    def delete_product(self, product_id: int) -> bool:
        """
        Удаление товара
        Возвращает True если удаление успешно, False если товар в заказе
        """
        # Проверяем, есть ли товар в заказах
        check_query = "SELECT COUNT(*) as count FROM OrderItems WHERE product_id = ?"
        result = self.execute_query(check_query, (product_id,))

        if result[0]["count"] > 0:
            return False

        delete_query = "DELETE FROM Products WHERE id = ?"
        self.execute_update(delete_query, (product_id,))
        return True

    def get_categories(self) -> List[Dict]:
        """Получение списка категорий"""
        return self.execute_query("SELECT id, name FROM Categories ORDER BY name")

    def get_manufacturers(self) -> List[Dict]:
        """Получение списка производителей"""
        return self.execute_query("SELECT id, name FROM Manufacturers ORDER BY name")

    def get_suppliers(self) -> List[Dict]:
        """Получение списка поставщиков"""
        return self.execute_query("SELECT id, name FROM Suppliers ORDER BY name")
