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
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model();  CustomUser.objects.create_superuser('admin1', 'admin1@gmail.com', 'teamlab')" | python manage.py shell
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model();  CustomUser.objects.create_superuser('admin2', 'admin2@gmail.com', 'teamlab')" | python manage.py shell
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model();  CustomUser.objects.create_superuser('admin3', 'admin3@gmail.com', 'teamlab')" | python manage.py shell
echo "from teacher.models import User; user = User.objects.create_user(username='hong1@naver.com', password='1431'); user.last_name='홍'; user.first_name='길동1'; user.teacher_id='1'; user.save()" | python manage.py shell

exec "$@"