FROM python:3.10

WORKDIR /app


RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app
COPY . /app

RUN poetry install

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080"]