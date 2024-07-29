FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/venv \
    PATH="/venv/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

FROM base AS build

ARG POETRY_VERSION=1.8.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install "poetry==$POETRY_VERSION" && \
    python -m venv /venv

WORKDIR /app/src

COPY pyproject.toml poetry.lock /app/src/

RUN poetry install --without dev --no-ansi --no-interaction

COPY src/cryptoapp /app/src/cryptoapp

FROM base AS final
COPY --from=build /venv /venv
WORKDIR /app/src
EXPOSE 8000
CMD ["uvicorn", "cryptoapp.main.web:create_app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--factory"]