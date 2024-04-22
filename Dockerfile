FROM arm64v8/python:3.11.8-slim-bullseye

RUN pip install poetry
RUN mkdir -p /app
COPY AtralAdmin ./app

WORKDIR /app

RUN poetry install --without dev
ENTRYPOINT ["poetry", "run", "python", "-m", "main.py"]