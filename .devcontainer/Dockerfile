FROM python:3.13-slim

ENV PYTHONPATH=${PYTHONPATH:-}:/workspace/src

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . .