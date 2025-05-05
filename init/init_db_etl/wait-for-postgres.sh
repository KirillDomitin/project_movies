#!/bin/bash

log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - $1"
}

set -e  # Остановить скрипт при ошибке

host="$1"
shift
cmd="$@"

log_info "Ожидание PostgreSQL ($host)..."

log_info "Ждём создания таблиц..."
sleep 5

log_info "Таблицы найдены, запускаем приложение!"
exec $cmd
