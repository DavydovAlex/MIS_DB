#!/bin/sh
grep -v pkg_resources requirements.txt > req_tmp.txt
cat req_tmp.txt > requirements.txt; rm req_tmp.txt
pip install --upgrade pip
pip install -r requirements.txt
apt-get update && apt-get -yq install unzip
apt-get install libaio1
cd /app
unzip instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip
mkdir -p /opt/oracle/instantclient_21_9
mv instantclient_21_9 /opt/oracle
chown -R root:root /opt/oracle/instantclient_21_9
cp TNSNAMES.ORA /opt/oracle/instantclient_21_9/network/admin
cd /app/mis
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8080