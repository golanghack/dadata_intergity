FROM public.ecr.aws/docker/library/python:3.12.8-slim

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.8.5

RUN apt-get update && \
  apt-get install --no-install-recommends -y postgresql postgresql-contrib libpq-dev gcc musl-dev libc-dev libffi-dev libssl-dev wget make wait-for-it\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . /app/

EXPOSE 8000
