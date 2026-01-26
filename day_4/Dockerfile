FROM python:3.14.2-slim

WORKDIR /app

ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv sync

COPY main.py main.py

ENTRYPOINT ["fastapi", "run", "/app/main.py", "--port", "8080"]
