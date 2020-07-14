FROM python:3.7.5-slim

# set work directory
WORKDIR /usr/src/sentence-analysis

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y \
            gcc python3-dev musl-dev netcat \
            libpq-dev postgresql-client postgresql-client-common \
            default-jre

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/sentence-analysis/requirements.txt
RUN pip install -r /usr/src/sentence-analysis/requirements.txt
RUN pip install django-cors-headers
RUN pip install gevent
RUN pip install gevent-websocket

# copy project
COPY . /usr/src/app/

EXPOSE 5252
ENTRYPOINT ["python", "/usr/src/app/server.py"]
