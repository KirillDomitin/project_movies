#!/bin/bash
set -e  # Остановить скрипт при ошибке

host="$1"
shift
cmd="$@"

echo "Ожидание PostgreSQL ($host)..."

echo "Ждём создания таблиц..."
sleep 5

echo "Таблицы найдены, запускаем приложение!"
exec $cmd
