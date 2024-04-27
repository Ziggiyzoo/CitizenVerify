FROM arm64v8/python:3.11.8-slim-bullseye

RUN pip install poetry
RUN mkdir -p /app
COPY AstralAdmin ./app
COPY pyproject.toml ./app

WORKDIR /app

RUN poetry install --without dev
ENTRYPOINT ["poetry", "run", "python",  "/AstralAdmin/main.py"]