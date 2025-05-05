import logging
from typing import List, Dict

from elasticsearch import Elasticsearch, helpers

logger = logging.getLogger(__name__)


class ElasticLoader:
    def __init__(self, client: Elasticsearch, index: str):
        self.index = index
        self.client = client

    def ensure_index(self, mapping: Dict):
        if not self.client.indices.exists(index=self.index):
            logger.info(f"Creating index '{self.index}' in Elasticsearch")
            self.client.indices.create(index=self.index, body={"mappings": mapping})
        else:
            logger.info(f"Index '{self.index}' already exists")

    def load(self, documents: List[Dict]):
        if not documents:
            logger.info("No documents to load into Elasticsearch")
            return

        actions = [
            {"_index": self.index, "_id": doc["id"], "_source": doc}
            for doc in documents
        ]

        logger.info(
            f"Loading {len(actions)} documents into Elasticsearch index '{self.index}'"
        )
        success, errors = helpers.bulk(self.client, actions, raise_on_error=False)

        logger.info(f"Bulk load completed: {success} successful operations")
        if errors:
            logger.warning(f"{len(errors)} errors occurred during bulk load")
            for error in errors:
                logger.debug(error)
