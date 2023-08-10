# Step #1 | Building an image
FROM python:3.9-slim-bullseye as build-image

# Step #2 | Files, variables and groups
# PYTHONUNBUFFERED - Log buffering in container stdout and stderr - 0 disable
# Adding to the docker group to be able to use docker commands without root in the future

ENV APP_ROOT /src
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:${APP_ROOT}"
ENV APP_USER service_user

RUN groupadd -r docker \
    && useradd -r -m \
    --home-dir ${APP_ROOT} \
    -s /usr/sbin/nologin \
    -g docker ${APP_USER}
RUN usermod -aG sudo ${APP_USER}

# Step #3 Installing poetry
# Do not create venv when installing poetry, but load dependencies into the python environment
FROM build-image as poetry-init

ARG APP_ROOT

WORKDIR ${APP_ROOT}

RUN pip install --no-cache-dir poetry==1.5.1

RUN poetry config virtualenvs.create false


# Step #4 | Installing dependencies
FROM poetry-init as poetry-install

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry install

# Step #5 | Application launch
FROM poetry-install as run-app

# . -> APP_ROOT /src
COPY . .

CMD ["alembic", "upgrade", "head"]

CMD ["uvicorn", "app.core.application:application", "--host", "0.0.0.0", "--port", "4000"]
