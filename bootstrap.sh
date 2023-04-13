#!/bin/sh

apt-get update && apt-get -yq install unzip

cd /app
unzip instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip
mv instantclient_21_9 /opt/oracle
cd /app/mis
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8080