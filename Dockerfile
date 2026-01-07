FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim as builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy
ENV UV_NO_DOWNLOAD_PYTHON=1

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev
COPY . .
RUN uv sync 

FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 999 user && \
    useradd --system --gid 999 --uid 999 --create-home user

WORKDIR /app

COPY --from=builder --chown=user:user /app/.venv /app/.venv
COPY --from=builder --chown=user:user . /app

ENV PATH="/app/.venv/bin:$PATH"

USER user
EXPOSE 7000

CMD [ "uv", "run", "main.py" ]