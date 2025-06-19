# syntax=docker/dockerfile:1
FROM python:3.13.3-alpine
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN apk add postgresql-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install starlette==0.46.2 --upgrade