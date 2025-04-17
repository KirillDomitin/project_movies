from typing import List, Dict, Any


class FilmworkTransformer:
    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.raw_data = raw_data

    def transform(self) -> List[Dict[str, Any]]:
        result = {}

        for row in self.raw_data:
            fw_id = str(row["fw_id"])

            if fw_id not in result:
                result[fw_id] = {
                    "id": fw_id,
                    "imdb_rating": row["rating"],
                    "title": row["title"],
                    "description": row["description"],
                    "genres": set(),
                    "directors": {},
                    "actors": {},
                    "writers": {},
                    "directors_names": set(),
                    "actors_names": set(),
                    "writers_names": set(),
                }

            # Добавляем жанр
            result[fw_id]["genres"].add(row["name"])

            # Собираем персону
            person_id = str(row["id"])
            person_name = row["full_name"]
            person_obj = {"id": person_id, "name": person_name}

            if row["role"] == "actor":
                result[fw_id]["actors"][person_id] = person_obj
                result[fw_id]["actors_names"].add(person_name)
            elif row["role"] == "director":
                result[fw_id]["directors"][person_id] = person_obj
                result[fw_id]["directors_names"].add(person_name)
            elif row["role"] == "writer":
                result[fw_id]["writers"][person_id] = person_obj
                result[fw_id]["writers_names"].add(person_name)

        # Финальное приведение к спискам
        for fw in result.values():
            fw["genres"] = list(fw["genres"])
            fw["actors"] = list(fw["actors"].values())
            fw["directors"] = list(fw["directors"].values())
            fw["writers"] = list(fw["writers"].values())
            fw["actors_names"] = list(fw["actors_names"])
            fw["directors_names"] = list(fw["directors_names"])
            fw["writers_names"] = list(fw["writers_names"])

        return list(result.values())
