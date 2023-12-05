# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
FROM python:3.8

WORKDIR /app
RUN apt-get update 
COPY ./requirements.txt /app/requirements.txt
USER root
RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt \
&& rm -rf /root/.cache/pip
RUN pip install --upgrade fastapi python-multipart

COPY . /app

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0","--port", "8000"]