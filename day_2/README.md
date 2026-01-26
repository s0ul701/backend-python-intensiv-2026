# Day 2: Pydantic и API

Демо-приложение для лекции "День 2: Pydantic и API"

## Что демонстрирует

- **Pydantic модели** для валидации входных данных
- **OpenAPI** автоматическая документация
- **Dependency Injection** для управления зависимостями
- **CRUD операции** с правильными HTTP статус-кодами

## Структура проекта

```
day_2/
├── app/
│   ├── __init__.py
│   ├── main.py           # Точка входа, создание FastAPI app
│   ├── config.py         # Настройки из YAML + env переменных
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py       # Pydantic модели UserResponse, UserUpdate
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── database.py   # In-memory БД и get_db dependency
│   └── routers/
│       ├── __init__.py
│       └── users.py      # CRUD эндпоинты для /users
├── config.yaml           # Конфигурация приложения
├── pyproject.toml        # Зависимости и настройки проекта
├── uv.lock               # Lock-файл зависимостей
└── README.md
```

## Быстрый старт

### 1. Установите uv (если ещё не установлен)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Установите зависимости

```bash
cd day_2
uv sync
```

Эта команда автоматически создаст виртуальное окружение и установит все зависимости из `pyproject.toml`.

### 3. Запустите сервер

```bash
uv run uvicorn app.main:app --reload
```

Сервер запустится на `http://localhost:8000`

### 4. Откройте документацию

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Примеры запросов

### Создать пользователя

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "name": "Alice", "age": 25}'
```

### Получить всех пользователей

```bash
curl "http://localhost:8000/users/"
```

### Получить пользователя по ID

```bash
curl "http://localhost:8000/users/1"
```

### Обновить пользователя

```bash
curl -X PATCH "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated"}'
```

### Удалить пользователя

```bash
curl -X DELETE "http://localhost:8000/users/1"
```

## Ключевые концепции

### Pydantic модели

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int | None = None
```

### Dependency Injection

```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def get_users(db: Database = Depends(get_db)):
    return db.get_all_users()
```

### Response Model

```python
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # FastAPI автоматически:
    # 1. Валидирует входные данные через UserCreate
    # 2. Фильтрует выходные данные через UserResponse
    # 3. Документирует в OpenAPI
    ...
```

## Конфигурация

Настройки читаются из `config.yaml`:

```yaml
app_name: "User Service API"
app_version: "1.0.0"
debug: false
log_level: "INFO"
host: "0.0.0.0"
port: 8000
```

Переменные окружения имеют приоритет над YAML:

```bash
# Переопределить уровень логирования
LOG_LEVEL=DEBUG uv run uvicorn app.main:app --reload
```

## Полезные команды

```bash
# Добавить зависимость
uv add <package>

# Добавить dev-зависимость
uv add --dev <package>

# Запустить тесты
uv run pytest

# Проверка кода линтером
uv run ruff check .

# Форматирование кода
uv run ruff format .
```

## Полезные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)