class PostgresEnricher:
    def __init__(self, conn, table_name, updated_data):
        self.cursor = conn.cursor()
        self.table_name = table_name
        self.intermediate_table = f"content.{table_name}_film_work"
        self.updated_data = updated_data
        self.offset = 0

    def get_enriched_data(self):
        enriched_ids = []
        while True:
            placeholders = ", ".join(["%s"] * len(self.updated_data))
            query = f"""
                    SELECT fw.id
                    FROM content.film_work fw
                    LEFT JOIN {self.intermediate_table} dfw ON dfw.film_work_id = fw.id
                    WHERE dfw.{self.table_name}_id IN ({placeholders})
                    ORDER BY fw.modified_at
                    LIMIT 100
                    OFFSET {self.offset};
                    """
            self.cursor.execute(query, tuple(self.updated_data))
            result = self.cursor.fetchall()
            if not result:
                break
            enriched_ids += result
            self.offset += 100
        return tuple([i[0] for i in enriched_ids])
