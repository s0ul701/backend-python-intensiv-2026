# Weather Service

Демо-приложение для воркшопа по тестированию в рамках ШИФТ Интенсив 2026.

## Установка (uv)

uv sync

## Запуск тестов

uv run pytest -v

## Запуск с покрытием

uv run pytest --cov=app --cov-report=term-missing

## Только unit-тесты

uv run pytest tests/unit -v

## Только интеграционные тесты

uv run pytest tests/integration -v

## Docker

# Запустить тесты
docker compose run --rm test

# Запустить с покрытием
docker compose run --rm test-cov

# Запустить приложение
docker compose up app

## Запуск приложения

uv run uvicorn app.main:app --reload
