import json
import logging
import time

import requests

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "movies"
MAPPING_FILE = "default_mapping.json"


def wait_for_elasticsearch(timeout=60):
    logging.info("Waiting for Elasticsearch ...")
    for i in range(timeout):
        try:
            res = requests.get(f"{ES_HOST}/_cluster/health")
            if res.status_code == 200:
                logging.info("Elasticsearch is available.")
                return
        except Exception as e:
            logging.error(f"[{i + 1}/{timeout}] Not ready yet: {e}")
        time.sleep(1)
    logging.warning("Elasticsearch not reachable after timeout.")
    raise RuntimeError("Elasticsearch not reachable after timeout.")


def create_index_if_missing():
    try:
        r = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if r.status_code == 404:
            logging.info(f"Index '{INDEX_NAME}' does not exist. Creating...")
            with open(MAPPING_FILE, "r") as f:
                mapping = json.load(f)
            create = requests.put(f"{ES_HOST}/{INDEX_NAME}", json=mapping)
            logging.info(f"Index created: {create.status_code} - {create.text}")
        elif r.status_code == 200:
            logging.info(f"Index '{INDEX_NAME}' already exists.")
        else:
            logging.error(f"Unexpected response: {r.status_code} - {r.text}")
    except Exception as e:
        logging.error(f"Error checking/creating index: {e}")
        raise


if __name__ == "__main__":
    wait_for_elasticsearch()
    create_index_if_missing()
