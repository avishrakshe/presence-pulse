import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-presence-pulse-dev-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*','172.22.103.181','127.127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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

# Use signed cookies for sessions (no DB table needed)
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
