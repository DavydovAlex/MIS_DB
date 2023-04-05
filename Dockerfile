FROM python:3.8.10
WORKDIR /app
COPY requirements.txt .

RUN grep -v pkg_resources requirements.txt   > req_tmp.txt
RUN cat req_tmp.txt >requirements.txt; rm req_tmp.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY mis mis

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