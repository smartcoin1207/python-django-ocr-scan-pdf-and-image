FROM python:3.12
LABEL maintainer="yoshiMT2.com"

ENV PYTHONUNBUFFERED 1

RUN python -m venv /py && . /py/bin/activate
RUN apt-get update && apt-get install -y postgresql-client gcc g++ build-essential libpq-dev  poppler-utils
RUN /py/bin/pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN /py/bin/pip install -r /requirements.txt

# setuptoolsのインストールを追加
RUN /py/bin/pip install setuptools

RUN apt-get autoremove -y && apt-get clean

COPY . /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"

# コンテナ内で実行するコマンド
CMD ["sh", "-c", "python manage.py wait_for_db && \
                  python manage.py migrate && \
                  (python manage.py qcluster &) && \
                  python manage.py runserver 0.0.0.0:80"]