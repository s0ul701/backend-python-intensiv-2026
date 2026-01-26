import logging
from datetime import datetime
from typing import Generator, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class UserModel:
    """Модель пользователя в 'базе данных'."""

    id: int
    email: str
    name: str
    age: int
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True


class Database:
    """Простая in-memory база данных для демонстрации."""

    def __init__(self):
        self._users: dict[int, UserModel] = {}
        self._next_id: int = 1
        self._connected: bool = True
        logger.info("Database connection opened")

    def close(self):
        """Закрыть подключение к базе."""
        self._connected = False
        logger.info("Database connection closed")

    def user_exists(self, email: str) -> bool:
        """Проверить, существует ли пользователь с таким email."""
        return any(user.email == email for user in self._users.values())

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Найти пользователя по email."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_user(self, user_id: int) -> Optional[UserModel]:
        """Получить пользователя по ID."""
        return self._users.get(user_id)

    def get_all_users(self) -> list[UserModel]:
        """Получить всех пользователей."""
        return list(self._users.values())

    def create_user(self, email: str, name: str, age: int) -> UserModel:
        """Создать нового пользователя."""
        user = UserModel(
            id=self._next_id, email=email, name=name, age=age, created_at=datetime.now()
        )
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        name: Optional[str] = None,
        age: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> Optional[UserModel]:
        """Обновить пользователя."""
        user = self._users.get(user_id)
        if not user:
            return None

        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if age is not None:
            user.age = age
        if is_active is not None:
            user.is_active = is_active

        return user

    def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя."""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


_db_instance: Optional[Database] = None


def get_db() -> Generator[Database, None, None]:
    """
    Dependency для получения подключения к базе данных.

    Использует yield для автоматического закрытия соединения после запроса.
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = Database()

    try:
        yield _db_instance
    finally:
        # В реальном проекте здесь закрывается сессия:
        # db.close()
        pass
