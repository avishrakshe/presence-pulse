import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-presence-pulse-dev-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['172.22.103.181']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'presencepulse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],  # serve HTML files from project root
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

WSGI_APPLICATION = 'presencepulse.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False
