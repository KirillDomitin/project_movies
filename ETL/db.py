import psycopg
from elasticsearch import Elasticsearch

from backoff import backoff


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
def get_pg_connection(dsn):
    return psycopg.connect(**dsn)


@backoff(start_sleep_time=1, factor=2, border_sleep_time=20)
def get_el_connection(elastic_host):
    return Elasticsearch(hosts=[elastic_host])
