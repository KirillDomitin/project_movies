CREATE SCHEMA IF NOT EXISTS content;

-- Таблица с информацией о фильмах
CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL, -- Название фильма
    description TEXT, -- Описание фильма
    creation_date DATE, -- Дата выхода фильма
    rating FLOAT CHECK (rating >= 0 AND rating <= 10), -- Рейтинг фильма от 0 до 10
    type VARCHAR(10) NOT NULL, -- Тип фильма (movie, series, tv show)
    certificate VARCHAR(512), -- Сертификат фильма
    file_path TEXT, -- Путь к файлу фильма
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, -- Дата создания записи
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL -- Дата последнего изменения
);

-- Таблица с жанрами
CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL, -- Название жанра
    description TEXT, -- Описание жанра
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, -- Дата создания записи
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL -- Дата последнего изменения
);

-- Таблица связи фильмов и жанров
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    genre_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES content.genre(id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE
);

-- Таблица с персоналиями
CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL, -- Полное имя
    gender TEXT CHECK (gender IN ('male', 'female')), -- Пол
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, -- Дата создания записи
    modified_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL -- Дата последнего изменения
);

-- Таблица связи персоналий и фильмов
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    person_id UUID NOT NULL,
    film_work_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL, -- Роль (actor, director, writer)
    FOREIGN KEY (person_id) REFERENCES content.person(id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work(id) ON DELETE CASCADE
);

-- Индексы для ускорения поиска
CREATE INDEX idx_film_work_type ON content.film_work (type); -- Индекс для ускорения поиска по типу фильма
CREATE INDEX idx_film_work_rating ON content.film_work (rating); -- Индекс для ускорения поиска по рейтингу

CREATE UNIQUE INDEX idx_genre_name ON content.genre (name); -- Уникальный индекс для названия жанра

CREATE INDEX idx_genre_film_work_genre_id ON content.genre_film_work (genre_id); -- Индекс для связи жанров с фильмами
CREATE INDEX idx_genre_film_work_film_work_id ON content.genre_film_work (film_work_id); -- Индекс для связи фильмов с жанрами

CREATE INDEX idx_person_full_name ON content.person (full_name); -- Индекс для быстрого поиска персон по имени

CREATE INDEX idx_person_film_work_person_id ON content.person_film_work (person_id); -- Индекс для связи персон с фильмами
CREATE INDEX idx_person_film_work_film_work_id ON content.person_film_work (film_work_id); -- Индекс для связи фильмов с персонами