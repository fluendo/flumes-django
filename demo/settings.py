from distutils.version import StrictVersion
from os import path

import django

from flumes_django.config import FlumesDjangoConfig

config = FlumesDjangoConfig()

DJANGO_VERSION = StrictVersion(django.get_version())

DEBUG = True
TEMPLATE_DEBUG = True
USE_TZ = True
USE_L10N = True

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "demo.db"},
    "flumes": {
        "ENGINE": config.get_django_database_engine(),
        "NAME": config.get_database_database(),
    },
}

DATABASE_ROUTERS = ["flumes_django.router.Router"]


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "flumes_django",
)

MIDDLEWARE = [
    # default django middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

PROJECT_DIR = path.abspath(path.join(path.dirname(__file__)))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
            ]
        },
    }
]

STATIC_URL = "/static/"

SECRET_KEY = "secret"  # noqa: S105

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "propagate": True, "level": "DEBUG"},
    },
}

ROOT_URLCONF = "demo.urls"

if not DEBUG:
    raise Exception("This settings file can only be used with DEBUG=True")
