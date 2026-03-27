from enum import Enum


class UserRole(Enum):
    """Роли пользователей"""

    ADMIN = "Администратор"
    MANAGER = "Менеджер"
    CLIENT = "Авторизированный клиент"
    GUEST = "Гость"


class User:
    """Модель пользователя"""

    def __init__(self, user_data: dict = None):
        if user_data:
            self.id = user_data.get("id")
            self.login = user_data.get("login")
            self.password = user_data.get("password")
            self.full_name = user_data.get("full_name")
            self.role_id = user_data.get("role_id")
            self.role_name = user_data.get("role_name")
        else:
            self.id = None
            self.login = ""
            self.password = ""
            self.full_name = "Гость"
            self.role_id = None
            self.role_name = "Гость"

    @property
    def role(self) -> UserRole:
        """Получение роли в виде Enum"""
        if self.role_name == "Администратор":
            return UserRole.ADMIN
        elif self.role_name == "Менеджер":
            return UserRole.MANAGER
        elif self.role_name == "Авторизированный клиент":
            return UserRole.CLIENT
        return UserRole.GUEST

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def is_manager(self) -> bool:
        return self.role == UserRole.MANAGER

    @property
    def is_client(self) -> bool:
        return self.role == UserRole.CLIENT

    @property
    def is_guest(self) -> bool:
        return self.role == UserRole.GUEST
