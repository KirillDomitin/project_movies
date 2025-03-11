# Укажите необходимую версию python
FROM python:3.12-slim

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /src

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PORT=8000

# Устанавливаем системные зависимости, необходимые для uWSGI
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы, которые редко меняются
COPY run_uwsgi.sh run_uwsgi.sh
COPY README.md README.md
COPY uwsgi/uwsgi.ini uwsgi.ini

# Делаем run_uwsgi.sh исполняемым
RUN chmod +x run_uwsgi.sh

RUN mkdir -p /app/staticfiles

# Устанавливаем Poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry --version

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock /src/

# Отключаем создание виртуального окружения и устанавливаем зависимости
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

# Устанавливаем uwsgi явно (если Poetry не подтянет)
RUN pip install uwsgi

# Копируем весь проект
COPY . .

# Указываем порт, на котором приложение будет доступно
EXPOSE ${PORT}

# Запуск сервера
CMD ["./entrypoint.sh"]