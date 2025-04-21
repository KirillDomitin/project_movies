import logging
from datetime import datetime

from psycopg import Connection
from psycopg.errors import Error, OperationalError

logger = logging.getLogger(__name__)


class ETLStateManager:
    def __init__(self, conn: Connection):
        self.conn = conn

    def get_last_sync(self, table: str) -> datetime:
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT last_modified FROM etl_state WHERE table_name = %s",
                    (table,)
                )
                row = cur.fetchone()
                if row:
                    logger.info(f"Database state for '{table}': {row[0]}")
                    return row[0]
                return datetime.min
        except (Error, OperationalError) as e:
            logger.warning(f"PostgreSQL unavailable. Using local state: {e}")
            raise
        # return datetime.min

    def set_last_sync(self, table: str, value: datetime):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO etl_state (table_name, last_modified)
                    VALUES (%s, %s)
                    ON CONFLICT (table_name) DO UPDATE
                    SET last_modified = EXCLUDED.last_modified;
                """, (table, value.isoformat()))
            logger.info(f"Updated state for '{table}': {value.isoformat()}")
        except (Error, OperationalError) as e:
            logger.warning(f"Failed to update PostgreSQL: {e}")
