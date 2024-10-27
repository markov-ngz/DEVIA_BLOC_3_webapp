FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./slovo /app

WORKDIR /app

COPY ./entrypoint.sh /

RUN sed -i 's/\r//g' /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN mkdir -p logs \
    && chown -R appuser:appgroup logs \
    && chmod -R 755 logs \
    && mkdir -p static \
    && chown -R appuser:appgroup static \ 
    && chmod -R 755 static \
    && chmod -R 777 translation

USER appuser 

ENTRYPOINT ["sh","/entrypoint.sh"]
