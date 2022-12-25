# syntax=docker/dockerfile:1
FROM python:3.10.6
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# SQLITE
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/test.db
CMD /bin/bash

# geospatial libraries
RUN apt-get install -y binutils libproj-dev gdal-bin

# libspatialite
RUN apt-get install -y libsqlite3-mod-spatialite

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000  
# RUN python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
