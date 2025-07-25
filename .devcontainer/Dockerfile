FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY pyproject.toml .
COPY uv.lock .

RUN uv venv
RUN uv sync --frozen


ENV PYTHONPATH=${PYTHONPATH:-}:/workspace/src

COPY . .