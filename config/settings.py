
import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

from config.config import config  # noqa: E402
from config.essentials import is_docker
from config.logginf_conf import logging_config  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent.parent
if not is_docker():
    load_dotenv(Path(BASE_DIR.parent, ".env"))



SECRET_KEY = config.app.SECRET_KEY
DEBUG = config.app.DEBUG

ALLOWED_HOSTS = config.app.ALLOWED_HOSTS

CORS_ALLOW_ALL_ORIGINS = config.cors.CORS_ALLOW_ALL_ORIGINS
CORS_ALLOW_CREDENTIALS = config.cors.CORS_ALLOW_CREDENTIALS
CORS_ORIGIN_WHITELIST = config.cors.CORS_ORIGIN_WHITELIST
CORS_ALLOW_HEADERS = list(default_headers) + [
    "*",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Credentials",
    "X-Amz-Date",
    "Access-Control-Request-Headers",
    "XMLHttpRequest",
    "X-Authorization",
]

CSRF_ALLOWED_ORIGINS = config.cors.CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = config.cors.CSRF_TRUSTED_ORIGINS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.migrations",
    # local
    "devices.apps.DevicesConfig",
    "registration.apps.RegistrationConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if is_docker():
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config.database.DB_NAME,
            "USER": config.database.DB_USER,
            "PASSWORD": config.database.DB_PASS,
            "HOST": config.database.DB_HOST,
            "PORT": config.database.DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Django rest framework configs
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
     'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication",
    ],
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


ADMIN_PANEL_URL = config.app.ADMIN_PANEL_URL.strip()
if ADMIN_PANEL_URL[-1] != "/":
    ADMIN_PANEL_URL += "/"

# drf-spectacular
# https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings

SPECTACULAR_SETTINGS = {
    "TITLE": "Dadata integration API",
    "DESCRIPTION": "Интергация с сервисом Dadata",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v1/",
    "COMPONENT_SPLIT_REQUEST": True,
    "DEFAULT_GENERATOR_CLASS": "config.swagger.schema.CustomSchemaGenerator",
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = logging_config
PASSWORD_RESET_TIMEOUT = config.app.PASSWORD_RESET_TIMEOUT


GUNICORN_WORKERS = config.gunicorn.GUNICORN_WORKERS
GUNICORN_THREADS = config.gunicorn.GUNICORN_THREADS
GUNICORN_LOGLEVEL = config.gunicorn.GUNICORN_LOGLEVEL
GUNICORN_BACKLOG = config.gunicorn.GUNICORN_BACKLOG
GUNICORN_WORKER_CONNECTIONS = config.gunicorn.GUNICORN_WORKER_CONNECTIONS
GUNICORN_MAX_REQUESTS = config.gunicorn.GUNICORN_MAX_REQUESTS
GUNICORN_MAX_REQUESTS_JITTER = config.gunicorn.GUNICORN_MAX_REQUESTS_JITTER
GUNICORN_GRACEFUL_TIMEOUT = config.gunicorn.GUNICORN_GRACEFUL_TIMEOUT
GUNICORN_KEEPALIVE = config.gunicorn.GUNICORN_KEEPALIVE

JWT_SECRET_KEY = config.app.SECRET_KEY


