FROM python:3.12-slim

RUN mkdir /TASK_fastapi_app

WORKDIR /TASK_fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
