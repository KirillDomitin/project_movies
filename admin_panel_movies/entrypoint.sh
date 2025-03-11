#!/bin/bash

set -e  # Остановить выполнение при ошибке

echo "🚀 Запуск entrypoint.sh..."

# Применяем миграции
echo "🔄 Применяем миграции..."
python manage.py migrate

# Создаём суперпользователя (если нужно)
if [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "👤 Создаём суперпользователя..."
    python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser(email='$DJANGO_SUPERUSER_EMAIL', username='admin', password='$DJANGO_SUPERUSER_PASSWORD')
EOF
fi

# Собираем статику
echo "🎨 Собираем статику..."
python manage.py collectstatic --noinput

# Запускаем сервер
echo "🚀 Запускаем Django!"
exec uwsgi --strict --ini uwsgi.ini
