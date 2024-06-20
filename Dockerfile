FROM arm64v8/python:3.11.8-slim-bullseye

RUN pip install poetry

ARG token
ENV TOKEN=$token

ARG sc_api_key
ENV SC_API_KEY=$sc_api_key

ARG firebase_secret
ENV FIREBASE_SECRET=$firebase_secret

ARG deployment_env
ENV DEPLOYMENT_ENV=$deployment_env

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cachez


RUN mkdir -p ./app
RUN mkdir -p /app/logs

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY AstralAdmin ./app
RUN ls ./app

WORKDIR /app

ENTRYPOINT ["poetry", "run", "python", "main.py"]