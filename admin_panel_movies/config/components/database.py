# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import os

CONTENT_SCHEMA = os.getenv("CONTENT_SCHEMA")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 5432),
        'OPTIONS': {
            # Явно указываем схемы, с которыми будет работать приложение.
            'options': f'-c search_path=public,{CONTENT_SCHEMA}'
        }
    }
}
