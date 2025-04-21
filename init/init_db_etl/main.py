import logging
import os

from db_engine import SqliteEngine, PostgresEngine
from utils import prepare_data

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Параметры подключения
DB_PATH = "db.sqlite"
DSN = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}
BATCH_SIZE = 100
SCHEMA = "content"


def migrate_table(
    sqlite_engine: SqliteEngine, postgres_engine: PostgresEngine, table: str
):
    """
    Переносит данные из SQLite в PostgreSQL для одной таблицы.
    :param sqlite_engine: Экземпляр SQLite движка.
    :param postgres_engine: Экземпляр PostgreSQL движка.
    :param table: Название таблицы.
    """
    pg_table = f"{SCHEMA}.{table}"
    logging.info(f"Миграция таблицы: {table}")

    # Очистка таблицы в PostgreSQL перед записью
    # postgres_engine.clear_table(table)

    for batch in sqlite_engine.fetch_records(table_name=table, batch_size=BATCH_SIZE):
        if not batch:
            break

        prepared_data = prepare_data(table, batch)
        postgres_engine.insert_data(table_name=pg_table, data=prepared_data)
        logging.info(f"Вставлено {len(prepared_data)} записей в {table}")


def main():
    """Основная функция для миграции данных."""
    logging.info("Запуск миграции данных")

    sqlite_engine = SqliteEngine(DB_PATH)
    postgres_engine = PostgresEngine(DSN)

    # Получаем и сортируем таблицы по длине их имен
    sqlite_tables = sorted(sqlite_engine.get_tables(), key=len)
    logging.info(f"Найдено {len(sqlite_tables)} таблиц для миграции")

    for table_name in sqlite_tables:
        migrate_table(sqlite_engine, postgres_engine, str(table_name))

    sqlite_engine.close()
    postgres_engine.close()
    logging.info("Миграция данных завершена")


if __name__ == "__main__":
    main()
