FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update &&  \
    apt-get install -y libpq-dev gcc && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]