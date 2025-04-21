import logging
import time

from const import DSN, tables, ELASTIC_HOST
from db import get_pg_connection, get_el_connection
from etl_components import (
    PostgresProducer,
    PostgresEnricher,
    PostgresMerger,
    FilmworkTransformer,
    ElasticLoader,
)
from state_manager import ETLStateManager

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


def create_state_table():
    logger.info(DSN)
    with get_pg_connection(DSN) as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS etl_state (
            table_name TEXT PRIMARY KEY,
            last_modified TIMESTAMP NOT NULL);
            """
        )


def main():
    create_state_table()
    while True:
        try:
            pg_connection = get_pg_connection(DSN)
            elastic_connection = get_el_connection(ELASTIC_HOST)
            with pg_connection as conn, elastic_connection as client:
                for table_name in tables:
                    state_manager = ETLStateManager(conn)
                    last_modified = state_manager.get_last_sync(table_name)

                    # получаем измененные ID + last_modified
                    producer = PostgresProducer(conn, table_name, last_modified)
                    result = producer.get_updated_data()

                    if not result:
                        time.sleep(1)
                        continue

                    updated_ids = result["ids"]
                    last_modified = result["last_modified"]  # из реальных данных

                    # получение обогащенные данных
                    if table_name != "film_work":
                        enricher = PostgresEnricher(conn, table_name, updated_ids)
                        enriched_data = enricher.get_enriched_data()
                    else:
                        enriched_data = updated_ids

                    if not enriched_data:
                        time.sleep(1)
                        continue

                    # получение всех недостающих данных
                    merger = PostgresMerger(conn, enriched_data)
                    merged_data = merger.get_merged_data()

                    # преобразование данных для записи в Elasticsearch
                    transformer = FilmworkTransformer(merged_data)
                    documents = transformer.transform()

                    # запись в Elasticsearch
                    try:
                        loader = ElasticLoader(client, "movies")
                        loader.load(documents)
                    except BaseException as exc:
                        continue

                    # Сохраняем последнее seen modified_at
                    state_manager.set_last_sync(table_name, last_modified)
                    time.sleep(1)
        except Exception as exc:
            continue


if __name__ == "__main__":
    main()
