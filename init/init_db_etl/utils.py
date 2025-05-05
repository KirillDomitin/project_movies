from datetime import datetime, timezone

from data_classes import FilmWork, GenreFilmWork, PersonFilmWork, Genre, Person


def genre(row):
    return Genre(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        created_at=datetime.now(timezone.utc),
        modified_at=datetime.now(timezone.utc),
    )


def person(row):
    return Person(
        id=row["id"],
        full_name=row["full_name"],
        gender="male",
        created_at=datetime.now(timezone.utc),
        modified_at=datetime.now(timezone.utc),
    )


def film_work(row):
    return FilmWork(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        creation_date=row["creation_date"],
        type=row["type"],
        rating=row["rating"],
        certificate="",
        file_path=row["file_path"],
        created_at=datetime.now(timezone.utc),
        modified_at=datetime.now(timezone.utc),
    )


def genre_film_work(row):
    return GenreFilmWork(
        id=row["id"], genre_id=row["genre_id"], film_work_id=row["film_work_id"]
    )


def person_film_work(row):
    return PersonFilmWork(
        id=row["id"],
        role=row["role"],
        person_id=row["person_id"],
        film_work_id=row["film_work_id"],
    )


def prepare_data(table_name, rows):
    return [globals()[table_name](row) for row in rows]
