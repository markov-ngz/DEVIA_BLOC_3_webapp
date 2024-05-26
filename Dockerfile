FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./slovo /app

WORKDIR /app

COPY ./entrypoint.sh /

ENTRYPOINT ["sh","/entrypoint.sh"]
