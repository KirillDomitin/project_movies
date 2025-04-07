FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN pip install requests

CMD ["python", "init_elasticsearch.py"]