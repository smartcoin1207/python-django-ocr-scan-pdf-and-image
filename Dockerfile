FROM python:3.11
LABEL maintainer="yoshiMT2.com"

ENV PYTHONUNBUFFERED 1

RUN python -m venv /py && . /py/bin/activate
RUN apt-get update && apt-get install -y postgresql-client gcc g++ build-essential libpq-dev
RUN /py/bin/pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN /py/bin/pip install -r /requirements.txt
RUN apt-get autoremove -y && apt-get clean

COPY ./app /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"