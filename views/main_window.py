import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QComboBox, QPushButton, QHeaderView, QMessageBox,
                             QFrame, QAbstractItemView, QApplication)
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from models.user import User
from views.product_form import ProductForm


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.db = DatabaseManager()
        self.edit_window = None
        self.current_sort = "name"
        self.current_order = "ASC"
        self.init_ui()
        self.load_products()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Обувной магазин - Каталог товаров")
        self.setGeometry(100, 100, 1300, 750)

        # Установка иконки окна
        if os.path.exists("resources/Icon.png"):
            self.setWindowIcon(QIcon("resources/Icon.png"))
        elif os.path.exists("resources/icon.ico"):
            self.setWindowIcon(QIcon("resources/Icon.ico"))
        elif os.path.exists("resources/icon.icns"):
            self.setWindowIcon(QIcon("resources/Icon.icns"))

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Верхняя панель
        top_panel = QFrame()
        top_panel.setStyleSheet("background-color: #7FFF00;")
        top_layout = QHBoxLayout()
        top_panel.setLayout(top_layout)

        # ФИО пользователя
        user_label = QLabel(f"👤 Пользователь: {self.user.full_name}")
        user_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 12px; padding: 5px;")
        top_layout.addWidget(user_label)

        top_layout.addStretch()

        # Кнопка выхода
        logout_button = QPushButton("🚪 Выход")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                font-family: 'Times New Roman';
                padding: 5px 15px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        logout_button.clicked.connect(self.logout)
        top_layout.addWidget(logout_button)

        main_layout.addWidget(top_panel)

        # Панель инструментов (только для менеджера и администратора)
        if self.user.is_manager or self.user.is_admin:
            toolbar = QFrame()
            toolbar.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
            toolbar_layout = QHBoxLayout()
            toolbar.setLayout(toolbar_layout)

            # Поиск
            search_layout = QVBoxLayout()
            search_label = QLabel("🔍 Поиск:")
            search_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 10px;")
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Поиск по названию, артикулу, описанию...")
            self.search_input.setStyleSheet("font-family: 'Times New Roman'; padding: 5px; width: 250px;")
            self.search_input.textChanged.connect(self.on_search_changed)
            search_layout.addWidget(search_label)
            search_layout.addWidget(self.search_input)
            toolbar_layout.addLayout(search_layout)

            # Фильтр по поставщику
            filter_layout = QVBoxLayout()
            filter_label = QLabel("🏭 Фильтр по поставщику:")
            filter_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 10px;")
            self.supplier_filter = QComboBox()
            self.supplier_filter.setStyleSheet("font-family: 'Times New Roman'; padding: 5px; width: 200px;")
            self.supplier_filter.addItem("Все поставщики")
            self.load_suppliers()
            self.supplier_filter.currentTextChanged.connect(self.on_filter_changed)
            filter_layout.addWidget(filter_label)
            filter_layout.addWidget(self.supplier_filter)
            toolbar_layout.addLayout(filter_layout)

            # Сортировка
            sort_layout = QVBoxLayout()
            sort_label = QLabel("📊 Сортировка по количеству:")
            sort_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 10px;")
            self.sort_combo = QComboBox()
            self.sort_combo.addItems(["Без сортировки", "По возрастанию (мало)", "По убыванию (много)"])
            self.sort_combo.setStyleSheet("font-family: 'Times New Roman'; padding: 5px; width: 180px;")
            self.sort_combo.currentTextChanged.connect(self.on_sort_changed)
            sort_layout.addWidget(sort_label)
            sort_layout.addWidget(self.sort_combo)
            toolbar_layout.addLayout(sort_layout)

            toolbar_layout.addStretch()

            # Кнопка добавления товара (только для администратора)
            if self.user.is_admin:
                add_button = QPushButton("➕ Добавить товар")
                add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #00FA9A;
                        font-family: 'Times New Roman';
                        padding: 8px 20px;
                        font-weight: bold;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #00E68A;
                    }
                """)
                add_button.clicked.connect(self.add_product)
                toolbar_layout.addWidget(add_button)

            main_layout.addWidget(toolbar)

        # Таблица товаров
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Фото", "Наименование", "Категория", "Описание",
            "Производитель", "Поставщик", "Цена", "Кол-во", "Скидка"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Настройка ширины колонок
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)

        self.table.setColumnWidth(1, 100)

        # Двойной клик для редактирования (только администратор)
        if self.user.is_admin:
            self.table.doubleClicked.connect(self.edit_product)

        main_layout.addWidget(self.table)

        # Панель действий (для администратора)
        if self.user.is_admin:
            action_panel = QFrame()
            action_panel.setStyleSheet("background-color: #F5F5F5; border-top: 1px solid #E0E0E0;")
            action_layout = QHBoxLayout()
            action_panel.setLayout(action_layout)

            action_layout.addStretch()

            # Кнопка удаления
            self.delete_button = QPushButton("🗑 Удалить выбранный товар")
            self.delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF6B6B;
                    font-family: 'Times New Roman';
                    padding: 8px 20px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #FF5252;
                }
            """)
            self.delete_button.clicked.connect(self.delete_selected_product)
            action_layout.addWidget(self.delete_button)

            action_layout.addStretch()

            main_layout.addWidget(action_panel)

        # Статусная строка
        self.status_label = QLabel("Готов к работе")
        self.status_label.setStyleSheet("font-family: 'Times New Roman'; padding: 5px; color: #666666;")
        main_layout.addWidget(self.status_label)

        # Общие стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QTableWidget {
                font-family: 'Times New Roman';
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #7FFF00;
                font-family: 'Times New Roman';
                font-weight: bold;
                padding: 8px;
            }
            QPushButton {
                font-family: 'Times New Roman';
            }
        """)

    def load_suppliers(self):
        """Загрузка списка поставщиков для фильтра"""
        suppliers = self.db.get_suppliers_list()
        self.supplier_filter.addItems(suppliers)

    def get_sort_params(self) -> tuple:
        """Получение параметров сортировки"""
        if not hasattr(self, 'sort_combo'):
            return ("name", "ASC")

        sort_text = self.sort_combo.currentText()
        if sort_text == "По возрастанию (мало)":
            return ("quantity", "ASC")
        elif sort_text == "По убыванию (много)":
            return ("quantity", "DESC")
        else:
            return ("name", "ASC")

    def load_products(self):
        """Загрузка товаров в таблицу"""
        search = self.search_input.text() if hasattr(self, 'search_input') else ""
        supplier = self.supplier_filter.currentText() if hasattr(self, 'supplier_filter') else ""
        sort_by, sort_order = self.get_sort_params()

        try:
            products = self.db.get_all_products_filtered(search, supplier, sort_by, sort_order)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки товаров: {str(e)}")
            return

        self.table.setRowCount(len(products))
        self.status_label.setText(f"Найдено товаров: {len(products)}")

        for row, product in enumerate(products):
            # ID
            id_item = QTableWidgetItem(str(product.get('id', '')))
            self.table.setItem(row, 0, id_item)

            # Фото
            image_path = product.get('image_path', 'resources/picture.png')
            if not image_path or not os.path.exists(image_path):
                image_path = 'resources/picture.png'

            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(90, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label = QLabel()
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(row, 1, image_label)
            else:
                self.table.setItem(row, 1, QTableWidgetItem("Нет фото"))

            # Наименование
            self.table.setItem(row, 2, QTableWidgetItem(product.get('name', '')))

            # Категория
            self.table.setItem(row, 3, QTableWidgetItem(product.get('category_name', '')))

            # Описание
            desc = product.get('description', '')
            desc_display = desc[:80] + '...' if len(desc) > 80 else desc
            self.table.setItem(row, 4, QTableWidgetItem(desc_display))

            # Производитель
            self.table.setItem(row, 5, QTableWidgetItem(product.get('manufacturer_name', '')))

            # Поставщик
            self.table.setItem(row, 6, QTableWidgetItem(product.get('supplier_name', '')))

            # Цена
            price = product.get('price', 0)
            discount = product.get('discount', 0)
            final_price = price * (1 - discount / 100)

            if discount > 0:
                price_text = f"{price:.2f} ₽\n→ {final_price:.2f} ₽ (-{discount}%)"
            else:
                price_text = f"{price:.2f} ₽"
            self.table.setItem(row, 7, QTableWidgetItem(price_text))

            # Количество
            quantity = product.get('quantity', 0)
            quantity_item = QTableWidgetItem(str(quantity))
            if quantity == 0:
                quantity_item.setForeground(QColor(255, 0, 0))
            self.table.setItem(row, 8, quantity_item)

            # Скидка
            discount_item = QTableWidgetItem(f"{discount}%")
            if discount > 15:
                discount_item.setForeground(QColor(0, 128, 0))
            self.table.setItem(row, 9, discount_item)

            # Цвет фона
            bg_color = None
            if discount > 15:
                bg_color = QColor("#2E8B57")
            elif quantity == 0:
                bg_color = QColor("#ADD8E6")

            if bg_color:
                for col in range(10):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(bg_color)

    def on_search_changed(self):
        self.load_products()

    def on_filter_changed(self):
        self.load_products()

    def on_sort_changed(self):
        self.load_products()

    def add_product(self):
        if self.edit_window and self.edit_window.isVisible():
            QMessageBox.warning(self, "Предупреждение", "Окно редактирования уже открыто")
            return
        self.edit_window = ProductForm(self.db, self.user)
        self.edit_window.product_saved.connect(self.load_products)
        self.edit_window.show()

    def edit_product(self, index):
        if self.edit_window and self.edit_window.isVisible():
            QMessageBox.warning(self, "Предупреждение", "Окно редактирования уже открыто")
            return
        row = index.row()
        product_id = int(self.table.item(row, 0).text())
        self.edit_window = ProductForm(self.db, self.user, product_id)
        self.edit_window.product_saved.connect(self.load_products)
        self.edit_window.show()

    def delete_selected_product(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите товар для удаления")
            return

        product_id = int(self.table.item(current_row, 0).text())
        product_name = self.table.item(current_row, 2).text()

        reply = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Удалить товар '{product_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                success = self.db.delete_product(product_id)
                if success:
                    QMessageBox.information(self, "Успех", "Товар удален")
                    self.load_products()
                else:
                    QMessageBox.warning(self, "Ошибка", "Товар есть в заказах, удалить нельзя")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")

    def logout(self):
        reply = QMessageBox.question(
            self, "Подтверждение выхода",
            "Выйти из системы?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            from views.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()

    def closeEvent(self, event):
        if self.edit_window and self.edit_window.isVisible():
            self.edit_window.close()
        event.accept()