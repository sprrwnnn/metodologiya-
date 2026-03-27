import sys
import os
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QFileDialog,
    QMessageBox,
    QFormLayout,
    QGroupBox,
    QWidget,
    QScrollArea,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from models.user import User
from utils.image_handler import ImageHandler


class ProductForm(QDialog):
    """
    Форма добавления/редактирования товара
    Доступна только администратору
    """

    product_saved = pyqtSignal()  # Сигнал о сохранении товара

    def __init__(self, db: DatabaseManager, user: User, product_id: int = None):
        super().__init__()
        self.db = db
        self.user = user
        self.product_id = product_id
        self.image_handler = ImageHandler()
        self.temp_image_path = None
        self.old_image_path = None
        self.edit_window_opened = False  # Для контроля открытия нескольких окон
        self.init_ui()

        if product_id:
            self.load_product_data()
            self.setWindowTitle("Редактирование товара")
        else:
            self.setWindowTitle("Добавление нового товара")

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setMinimumWidth(700)
        self.setMinimumHeight(800)
        self.setModal(True)  # Модальное окно

        # Основной layout
        main_layout = QVBoxLayout()

        # Скролл-область (для длинных форм)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Группа с информацией о товаре
        info_group = QGroupBox("Информация о товаре")
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # ID (только для чтения при редактировании)
        if self.product_id:
            self.id_label = QLabel(str(self.product_id))
            self.id_label.setStyleSheet("color: #666666;")
            form_layout.addRow("ID товара:", self.id_label)

        # Артикул
        self.article_input = QLineEdit()
        self.article_input.setPlaceholderText("Введите артикул товара")
        self.article_input.setToolTip("Уникальный артикул товара (необязательно)")
        form_layout.addRow("Артикул:", self.article_input)

        # Наименование (обязательное)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование товара")
        self.name_input.setToolTip("Обязательное поле")
        form_layout.addRow("Наименование:*", self.name_input)

        # Категория
        self.category_combo = QComboBox()
        self.load_categories()
        form_layout.addRow("Категория:", self.category_combo)

        # Описание
        self.description_text = QTextEdit()
        self.description_text.setMaximumHeight(100)
        self.description_text.setPlaceholderText("Введите описание товара")
        form_layout.addRow("Описание:", self.description_text)

        # Производитель
        self.manufacturer_combo = QComboBox()
        self.load_manufacturers()
        form_layout.addRow("Производитель:", self.manufacturer_combo)

        # Поставщик
        self.supplier_combo = QComboBox()
        self.load_suppliers()
        form_layout.addRow("Поставщик:", self.supplier_combo)

        # Цена
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setMinimum(0)
        self.price_spin.setMaximum(1000000)
        self.price_spin.setDecimals(2)
        self.price_spin.setPrefix("₽ ")
        self.price_spin.setToolTip("Цена не может быть отрицательной")
        form_layout.addRow("Цена:*", self.price_spin)

        # Единица измерения
        self.unit_input = QLineEdit()
        self.unit_input.setText("шт")
        self.unit_input.setToolTip("Единица измерения товара")
        form_layout.addRow("Единица измерения:", self.unit_input)

        # Количество на складе
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(0)
        self.quantity_spin.setMaximum(100000)
        self.quantity_spin.setToolTip("Количество не может быть отрицательным")
        form_layout.addRow("Количество на складе:*", self.quantity_spin)

        # Скидка
        self.discount_spin = QSpinBox()
        self.discount_spin.setMinimum(0)
        self.discount_spin.setMaximum(100)
        self.discount_spin.setSuffix("%")
        self.discount_spin.setToolTip("Скидка от 0 до 100%")
        form_layout.addRow("Скидка:", self.discount_spin)

        info_group.setLayout(form_layout)
        scroll_layout.addWidget(info_group)

        # Группа с изображением
        image_group = QGroupBox("Изображение товара")
        image_layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setMinimumSize(300, 200)
        self.image_label.setMaximumSize(300, 200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            border: 2px dashed #CCCCCC;
            background-color: #F5F5F5;
        """)
        self.image_label.setText("Нет изображения\n\nНажмите 'Загрузить'")
        image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("📁 Загрузить изображение")
        self.upload_button.setToolTip("Выберите файл изображения (300x200 пикселей)")
        self.upload_button.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_button)

        if self.product_id:
            self.delete_image_button = QPushButton("🗑 Удалить изображение")
            self.delete_image_button.setToolTip("Удалить текущее изображение")
            self.delete_image_button.clicked.connect(self.delete_image)
            button_layout.addWidget(self.delete_image_button)

        image_layout.addLayout(button_layout)

        info_label = QLabel("* Поля, обязательные для заполнения")
        info_label.setStyleSheet("color: #666666; font-size: 10px;")
        image_layout.addWidget(info_label)

        image_group.setLayout(image_layout)
        scroll_layout.addWidget(image_group)

        # Кнопки сохранения и отмены
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("✓ Сохранить")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
                font-family: 'Times New Roman';
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
        """)
        self.save_button.clicked.connect(self.save_product)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("✗ Отмена")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                font-family: 'Times New Roman';
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        scroll_layout.addLayout(button_layout)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

        # Общий стиль
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                font-family: 'Times New Roman';
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #7FFF00;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
                border-color: #00FA9A;
            }
        """)

    def load_categories(self):
        """Загрузка категорий"""
        categories = self.db.get_categories()
        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])

    def load_manufacturers(self):
        """Загрузка производителей"""
        manufacturers = self.db.get_manufacturers()
        for manufacturer in manufacturers:
            self.manufacturer_combo.addItem(manufacturer["name"], manufacturer["id"])

    def load_suppliers(self):
        """Загрузка поставщиков"""
        suppliers = self.db.get_suppliers()
        for supplier in suppliers:
            self.supplier_combo.addItem(supplier["name"], supplier["id"])

    def load_product_data(self):
        """Загрузка данных товара для редактирования"""
        product = self.db.get_product_by_id(self.product_id)

        if product:
            self.article_input.setText(product.get("article", ""))
            self.name_input.setText(product["name"])

            # Установка категории
            index = self.category_combo.findData(product.get("category_id"))
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

            self.description_text.setText(product.get("description", ""))

            # Установка производителя
            index = self.manufacturer_combo.findData(product.get("manufacturer_id"))
            if index >= 0:
                self.manufacturer_combo.setCurrentIndex(index)

            # Установка поставщика
            index = self.supplier_combo.findData(product.get("supplier_id"))
            if index >= 0:
                self.supplier_combo.setCurrentIndex(index)

            self.price_spin.setValue(product["price"])
            self.unit_input.setText(product.get("unit", "шт"))
            self.quantity_spin.setValue(product["quantity"])
            self.discount_spin.setValue(product["discount"])

            # Загрузка изображения
            image_path = product.get("image_path")
            if image_path and os.path.exists(image_path):
                self.old_image_path = image_path
                self.temp_image_path = image_path
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(
                    300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.image_label.setPixmap(pixmap)
                self.image_label.setText("")

    def upload_image(self):
        """Загрузка изображения"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_path:
            try:
                # Проверяем, что файл - изображение
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    QMessageBox.warning(self, "Ошибка", "Файл не является изображением")
                    return

                self.temp_image_path = file_path
                pixmap = pixmap.scaled(
                    300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.image_label.setPixmap(pixmap)
                self.image_label.setText("")

            except Exception as e:
                QMessageBox.warning(
                    self, "Ошибка", f"Не удалось загрузить изображение: {str(e)}"
                )

    def delete_image(self):
        """Удаление изображения"""
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить изображение?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.temp_image_path = None
            self.image_label.clear()
            self.image_label.setText("Нет изображения\n\nНажмите 'Загрузить'")
            self.image_label.setStyleSheet("""
                border: 2px dashed #CCCCCC;
                background-color: #F5F5F5;
            """)

    def validate_data(self) -> bool:
        """Валидация данных"""
        # Проверка названия
        if not self.name_input.text().strip():
            QMessageBox.warning(
                self, "Ошибка", "Поле 'Наименование' обязательно для заполнения"
            )
            self.name_input.setFocus()
            return False

        # Проверка цены
        if self.price_spin.value() < 0:
            QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной")
            return False

        # Проверка количества
        if self.quantity_spin.value() < 0:
            QMessageBox.warning(
                self, "Ошибка", "Количество не может быть отрицательным"
            )
            return False

        # Проверка скидки
        if self.discount_spin.value() < 0 or self.discount_spin.value() > 100:
            QMessageBox.warning(self, "Ошибка", "Скидка должна быть от 0 до 100%")
            return False

        return True

    def save_product(self):
        """Сохранение товара"""
        if not self.validate_data():
            return

        try:
            # Определяем ID для сохранения изображения
            temp_id = self.product_id if self.product_id else self.get_next_id()

            # Сохраняем изображение
            final_image_path = None
            if self.temp_image_path:
                final_image_path = self.image_handler.save_product_image(
                    self.temp_image_path, temp_id
                )
            elif not self.product_id:
                final_image_path = self.image_handler.default_image

            # Подготовка данных
            product_data = {
                "article": self.article_input.text().strip() or None,
                "name": self.name_input.text().strip(),
                "description": self.description_text.toPlainText(),
                "category_id": self.category_combo.currentData(),
                "manufacturer_id": self.manufacturer_combo.currentData(),
                "supplier_id": self.supplier_combo.currentData(),
                "price": self.price_spin.value(),
                "unit": self.unit_input.text(),
                "quantity": self.quantity_spin.value(),
                "discount": self.discount_spin.value(),
                "image_path": final_image_path,
            }

            if self.product_id:
                # Обновление существующего товара
                # Удаляем старое изображение, если оно было заменено
                if (
                    self.old_image_path
                    and self.temp_image_path != self.old_image_path
                    and self.old_image_path != self.image_handler.default_image
                ):
                    self.image_handler.delete_image(self.old_image_path)

                self.db.update_product(self.product_id, product_data)
                QMessageBox.information(self, "Успех", "Товар успешно обновлен")
            else:
                # Добавление нового товара
                new_id = self.db.add_product(product_data)

                # Если изображение было загружено, сохраняем с правильным ID
                if (
                    self.temp_image_path
                    and final_image_path != self.image_handler.default_image
                ):
                    final_path = self.image_handler.save_product_image(
                        self.temp_image_path, new_id
                    )
                    self.db.update_product(new_id, {"image_path": final_path})

                QMessageBox.information(self, "Успех", "Товар успешно добавлен")

            self.product_saved.emit()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")

    def get_next_id(self) -> int:
        """Получение следующего ID для товара"""
        products = self.db.get_all_products()
        if products:
            return max(p["id"] for p in products) + 1
        return 1

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.edit_window_opened = False
        event.accept()
