FROM python:3.9-alpine3.13 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src
RUN mkdir -p /usr/src/app
RUN apk add --no-cache libmemcached-dev build-base postgresql-dev git jpeg-dev zlib-dev  \
    gettext gcc cairo-dev libwebp-dev curl postgresql-client

WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for
COPY / /app/
RUN chmod 777 entrypoint.sh