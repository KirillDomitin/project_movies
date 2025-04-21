from psycopg.rows import dict_row


class PostgresMerger:
    def __init__(self, conn, enriched_data):
        self.conn = conn
        self.cursor = conn.cursor(row_factory=dict_row)
        self.enriched_data = enriched_data

    def get_merged_data(self):

        placeholders = ", ".join(["%s"] * len(self.enriched_data))
        query = f"""
                SELECT
                    fw.id as fw_id,
                    fw.title,
                    fw.description,
                    fw.rating,
                    fw.type,
                    fw.created_at,
                    fw.modified_at,
                    pfw.role,
                    p.id,
                    p.full_name,
                    g.name
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.id IN ({placeholders});
                """
        self.cursor.execute(query, self.enriched_data)
        result = self.cursor.fetchall()
        return result
