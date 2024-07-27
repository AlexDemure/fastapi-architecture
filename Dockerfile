# Шаг №1 | Сборка образа
FROM python:3.12-slim-bullseye as build-image


# Шаг №2 Установка poetry
# Не создавать venv при poetry install, а загружать зависимости в python-окружение
FROM build-image as poetry-init

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

# Шаг №3 | Установка зависимостей
FROM poetry-init as poetry-install

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry install

# Шаг №4 | Запуск приложения
FROM poetry-install as run-app

COPY .env.example .env
# . -> APP_ROOT /srv/invoices/
COPY ./src /src

COPY cli.py .
