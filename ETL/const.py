import os

DSN = {
    "dbname": os.getenv("POSTGRES_DB", "movies_database"),
    "user": os.getenv("POSTGRES_USER", "app"),
    "password": os.getenv("POSTGRES_PASSWORD", "123qwe"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

tables = [
    "genre",
    "person",
    "film_work",
]

ELASTIC_HOST = f"http://{os.getenv('ELASTIC_HOST')}:{os.getenv('ELASTIC_PORT')}"
