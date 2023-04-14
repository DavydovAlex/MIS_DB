FROM python:3.8.10
WORKDIR /app

#COPY requirements.txt .

#COPY mis mis
#RUN unzip ${CLIENT_ZIP}
#ARG ORACLE_ZIP_INTERNAL_FOLDER=instantclient_21_9
#RUN mv ${ORACLE_ZIP_INTERNAL_FOLDER} /opt/oracle
#ENV ORACLE_HOME /opt/oracle
#ENV TNS_ADMIN ${ORACLE_HOME}/network/admin
#ENV PYTHONUNBUFFERED=1
#ENV DJANGO_SUPERUSER_USERNAME=admin
#ENV DJANGO_SUPERUSER_EMAIL=tst@gmail.com
#ENV DJANGO_SUPERUSER_PASSWORDpi=123

#WORKDIR /app/mis
#RUN python manage.py makemigrations
#RUN python manage.py migrate
#RUN python manage.py createsuperuser --noinput
#WORKDIR /app
#EXPOSE 8000

#CMD ["python", "mis/manage.py", "runserver"]