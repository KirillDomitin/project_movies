import logging

logger = logging.getLogger(__name__)


class PostgresProducer:
    def __init__(self, conn, table_name, last_modified):
        self.conn = conn
        self.cursor = conn.cursor()
        self.table_name = f"content.{table_name}"
        self.last_modified = last_modified

    def get_updated_data(self):
        logger.info(f"Checking for updates in table '{self.table_name}' after {self.last_modified.isoformat()}")

        query = f"""
            SELECT id, modified_at
            FROM {self.table_name}
            WHERE modified_at > %s
            ORDER BY modified_at
            LIMIT 100;
        """
        self.cursor.execute(query, (self.last_modified,))
        rows = self.cursor.fetchall()

        if not rows:
            logger.info(f"No new records found in '{self.table_name}'")
            return None

        ids = [row[0] for row in rows]
        last_modified = rows[-1][1]

        logger.info(
            f"Fetched {len(ids)} updated records from '{self.table_name}', latest modified_at: {last_modified.isoformat()}")
        return {"ids": ids, "last_modified": last_modified}
