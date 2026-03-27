import sys
import os
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from models.user import User
from views.main_window import MainWindow


class LoginWindow(QWidget):
    """Окно авторизации"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Авторизация - Обувной магазин")
        self.setFixedSize(450, 550)

        # Установка иконки
        if os.path.exists("resources/Icon.png"):
            self.setWindowIcon(QIcon("resources/Icon.png"))

        self.setStyleSheet("background-color: #FFFFFF; font-family: 'Times New Roman';")

        # Центрирование окна
        self.center()

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Логотип
        logo_label = QLabel()
        if os.path.exists("resources/Icon.png"):
            pixmap = QPixmap("resources/Icon.png")
            pixmap = pixmap.scaled(
                200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        # Заголовок
        title_label = QLabel("Вход в систему")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E8B57;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Поле логина
        login_layout = QVBoxLayout()
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("font-size: 12px;")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите email или логин")
        self.login_input.setStyleSheet(
            "padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;"
        )
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        main_layout.addLayout(login_layout)

        # Поле пароля
        password_layout = QVBoxLayout()
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet("font-size: 12px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "padding: 10px; border: 1px solid #CCCCCC; border-radius: 5px;"
        )
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #00FA9A;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00E68A;
            }
            QPushButton:pressed {
                background-color: #00D27A;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)

        # Кнопка входа как гость
        self.guest_button = QPushButton("Войти как гость")
        self.guest_button.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                padding: 12px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6EEB00;
            }
        """)
        self.guest_button.clicked.connect(self.handle_guest_login)
        main_layout.addWidget(self.guest_button)

        # Кнопка выхода
        self.exit_button = QPushButton("Выход")
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                padding: 12px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        self.exit_button.clicked.connect(self.close)
        main_layout.addWidget(self.exit_button)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def center(self):
        """Центрирование окна на экране"""
        screen = self.screen().geometry()
        self.move(screen.center() - self.rect().center())

    def handle_login(self):
        """Обработка входа"""
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        try:
            user_data = self.db.get_user_by_credentials(login, password)

            if user_data:
                self.current_user = User(user_data)
                self.open_main_window()
            else:
                QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения к БД: {str(e)}")

    def handle_guest_login(self):
        """Вход как гость"""
        self.current_user = User()
        self.open_main_window()

    def open_main_window(self):
        """Открытие главного окна"""
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
        self.hide()
