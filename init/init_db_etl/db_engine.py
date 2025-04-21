import logging
import sqlite3
from dataclasses import asdict
from typing import List

import psycopg

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SqliteEngine:
    """
    Класс для работы с базой данных SQLite.
    Позволяет подключаться, получать список таблиц, извлекать записи и закрывать соединение.
    """

    def __init__(self, db_path: str):
        """Инициализирует соединение с базой данных SQLite."""
        try:
            self.db_path = db_path
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при подключении к SQLite: {e}")

    def get_tables(self):
        """Возвращает список всех таблиц в базе данных."""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении списка таблиц: {e}")
            return []

    def fetch_records(self, table_name: str, batch_size: int = 100):
        """
        Генератор, который извлекает данные из указанной таблицы SQLite пачками.
        :param table_name: Название таблицы.
        :param batch_size: Размер батча.
        """
        try:
            query = f"SELECT * FROM {table_name};"
            self.cursor.execute(query)
            while True:
                batch = self.cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
        except sqlite3.Error as e:
            logging.error(f"Ошибка при извлечении данных из {table_name}: {e}")

    def close(self):
        """Закрывает соединение с базой данных SQLite."""
        try:
            self.cursor.close()
            self.connection.close()
        except sqlite3.Error as e:
            logging.error(f"Ошибка при закрытии соединения SQLite: {e}")


class PostgresEngine:
    """
    Класс для работы с базой данных PostgreSQL.
    Позволяет подключаться, очищать таблицы, вставлять данные и закрывать соединение.
    """

    def __init__(self, dsn: dict):
        """Инициализирует соединение с базой данных PostgreSQL."""
        try:
            self.connection = psycopg.connect(**dsn)
            self.cursor = self.connection.cursor()
            self.inserted_rows = 0  # Переменная для подсчета вставленных строк
        except psycopg.Error as e:
            logging.error(f"Ошибка при подключении к PostgreSQL: {e}")

    def clear_table(self, table_name: str):
        """
        Очищает содержимое указанной таблицы PostgreSQL.
        :param table_name: Название таблицы.
        """
        try:
            self.cursor.execute(
                f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"
            )
            self.connection.commit()
        except psycopg.Error as e:
            logging.error(f"Ошибка при очистке таблицы {table_name}: {e}")

    def insert_data(self, table_name: str, data: List):
        """
        Вставляет данные в указанную таблицу PostgreSQL.
        :param table_name: Название таблицы.
        :param data: Список записей (dataclass объектов) для вставки.
        """
        if not data:
            return

        try:
            columns = asdict(data[0]).keys()
            columns_str = ", ".join(columns)
            values_str = ", ".join([f"%s" for _ in columns])
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
            batch = [tuple(asdict(d)[col] for col in columns) for d in data]
            self.cursor.executemany(query, batch)
            self.connection.commit()
            self.inserted_rows += len(batch)
        except psycopg.Error as e:
            logging.error(f"Ошибка при вставке данных в {table_name}: {e}")
            self.connection.rollback()  # 🔥 Откатываем транзакцию, чтобы избежать блокировки

    def get_inserted_rows_count(self):
        """Возвращает количество успешно вставленных строк."""
        return self.inserted_rows

    def close(self):
        """Закрывает соединение с базой данных PostgreSQL."""
        try:
            logging.info(f"Всего вставлено строк: {self.inserted_rows}")
            self.cursor.close()
            self.connection.close()
        except psycopg.Error as e:
            logging.error(f"Ошибка при закрытии соединения PostgreSQL: {e}")
