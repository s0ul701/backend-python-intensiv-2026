import logging

from fastapi import FastAPI

from app.config import get_settings
from app.routers import users_router

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(
    f"Starting {settings.app_name} v{settings.app_version} on {settings.host}:{settings.port}"
)

app = FastAPI(
    title=settings.app_name,
    description="""
## Демо-приложение

Этот API демонстрирует использование:
- **Pydantic** для валидации данных
- **OpenAPI** для автоматической документации
- **Dependency Injection** для управления зависимостями

### Возможности
- Создание, чтение, обновление и удаление пользователей
- Автоматическая валидация email
- Проверка уникальности email
    """,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(users_router)


@app.get("/", tags=["root"])
def root():
    """
    Корневой эндпоинт.

    Возвращает приветственное сообщение и ссылки на документацию.
    """
    return {
        "message": "Добро пожаловать в User Service API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
    }
