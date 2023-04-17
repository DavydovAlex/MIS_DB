FROM python:3.8.10

ARG CLIENT=instantclient-basiclite-linux.x64-21.9.0.0.0dbru.zip

WORKDIR /app

COPY requirements.txt .
RUN grep -v pkg_resources requirements.txt > req_tmp.txt
RUN cat req_tmp.txt > requirements.txt; rm req_tmp.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get -yq install unzip
RUN apt-get install libaio1

COPY $CLIENT .
RUN unzip $CLIENT
RUN mkdir -p /opt/oracle/instantclient_21_9
RUN mv instantclient_21_9 /opt/oracle

COPY TNSNAMES.ORA  /opt/oracle/instantclient_21_9/network/admin
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