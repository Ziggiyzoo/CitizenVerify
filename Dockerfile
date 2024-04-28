FROM arm64v8/python:3.11.8-slim-bullseye

RUN pip install poetry

RUN --mount=type=secret,id=TOKEN \
    export TOKEN=$(cat /run/secrets/TOKEN)

RUN --mount=type=secret,id=SC_API_KEY \
    export SC_API_KEY=$(cat /run/secrets/SC_API_KEY)

RUN --mount=type=secret,id=FIREBASE_SECRET \
    export FIREBASE_SECRET=$(cat /run/secrets/FIREBASE_SECRET)

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cachez\
    TOKEN=${{secrets.TOKEN}} \
    SC_API_KEY=${{secrets.SC_API_KEY}} \
    FIREBASE_SECRET=${{secrets.FIREBASE_SECRET}}

RUN mkdir -p ./app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY AstralAdmin ./app
RUN ls ./app

WORKDIR /app

ENTRYPOINT ["poetry", "run", "python", "main.py"]