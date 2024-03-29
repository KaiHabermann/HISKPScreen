
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update
RUN apt-get install -y poppler-utils
RUN apt-get install -y iputils-ping
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/