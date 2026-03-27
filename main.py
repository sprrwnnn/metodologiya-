#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.login_window import LoginWindow


def main():
    """Главная функция запуска приложения"""
    app = QApplication(sys.argv)
    
    # Установка шрифта по умолчанию (Times New Roman)
    font = QFont("Times New Roman", 10)
    app.setFont(font)
    
    # Установка иконки приложения
    icon_paths = [
        "resources/icon.icns",
        "resources/icon.ico",
        "resources/icon.png",
        "resources/icon.jpeg"
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"Иконка загружена: {icon_path}")
            break
    else:
        print("Иконка не найдена. Используется стандартная.")
    
    # Создание и отображение окна авторизации
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()