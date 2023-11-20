FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY backend/pyproject.toml backend/poetry.lock /app/

RUN poetry install --no-root


COPY . /app

CMD gunicorn -k uvicorn.workers.UvicornWorker -b :8000 main:app

WORKDIR /app/backend
