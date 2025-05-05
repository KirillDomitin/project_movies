# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False) == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")
INTERNAL_IPS = os.getenv("DJANGO_INTERNAL_IPS").split(",")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
# Указываем папку для статики
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "ru-RU"
USE_TZ = True
TIME_ZONE = "UTC"
USE_I18N = True
