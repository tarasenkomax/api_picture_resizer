FROM python:3.10-alpine3.13 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_PATH "/app"

WORKDIR /usr/src
RUN mkdir -p /usr/src/app
RUN apk add --no-cache libmemcached-dev build-base postgresql-dev git jpeg-dev zlib-dev  \
    gettext gcc cairo-dev libwebp-dev curl postgresql-client

WORKDIR $PROJECT_PATH
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

RUN mkdir -p /app/media
RUN mkdir -p /app/logs
VOLUME ["/app/logs", "/app/media"]

COPY . $PROJECT_PATH