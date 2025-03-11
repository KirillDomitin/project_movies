FROM python:3.12-slim

WORKDIR app

COPY . /app

RUN apt-get update &&  \
    apt-get install -y libpq-dev gcc && \
    pip install -r requirements.txt

# Делаем скрипт исполняемым
RUN chmod +x /app/wait-for-postgres.sh

# Указываем рабочую директорию
ENTRYPOINT ["/wait-for-postgres.sh"]