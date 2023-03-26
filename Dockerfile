FROM python:3.6
WORKDIR /app
COPY requirements.txt .
RUN grep -v pkg_resources requirements.txt   > req_tmp.txt
RUN cat req_tmp.txt >requirements.txt; rm req_tmp.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY mis mis

ENV PYTHONUNBUFFERED=1
#EXPOSE 8000

#CMD ["python", "mis/manage.py", "runserver"]