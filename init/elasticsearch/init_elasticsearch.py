import json
import time
import requests

ES_HOST = "http://elasticsearch:9200"
INDEX_NAME = "movies"
MAPPING_FILE = "default_mapping.json"


def wait_for_elasticsearch(timeout=60):
    print("Waiting for Elasticsearch ...")
    for i in range(timeout):
        try:
            res = requests.get(f"{ES_HOST}/_cluster/health")
            if res.status_code == 200:
                print("Elasticsearch is available.")
                return
        except Exception as e:
            print(f"[{i + 1}/{timeout}] Not ready yet: {e}")
        time.sleep(1)
    raise RuntimeError("Elasticsearch not reachable after timeout.")


def create_index_if_missing():
    try:
        r = requests.head(f"{ES_HOST}/{INDEX_NAME}")
        if r.status_code == 404:
            print(f"Index '{INDEX_NAME}' does not exist. Creating...")
            with open(MAPPING_FILE, 'r') as f:
                mapping = json.load(f)
            create = requests.put(f"{ES_HOST}/{INDEX_NAME}", json=mapping)
            print(f"Index created: {create.status_code} - {create.text}")
        elif r.status_code == 200:
            print(f"Index '{INDEX_NAME}' already exists.")
        else:
            print(f"Unexpected response: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error checking/creating index: {e}")
        raise


if __name__ == "__main__":
    wait_for_elasticsearch()
    create_index_if_missing()
