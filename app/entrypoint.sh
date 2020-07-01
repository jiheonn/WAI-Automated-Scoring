#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete


python manage.py flush --no-input
python manage.py makemigrations 
python manage.py makemigrations mainpage
python manage.py makemigrations teacher
python manage.py migrate
python manage.py loaddata init_mainpage.json
python manage.py loaddata init_teacher.json
python manage.py collectstatic --no-input --clear

exec "$@"