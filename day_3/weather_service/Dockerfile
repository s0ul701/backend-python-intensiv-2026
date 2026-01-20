FROM python:3.11-slim

WORKDIR /app

ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./
COPY . .

RUN uv sync --extra dev

ENTRYPOINT ["uv", "run"]
