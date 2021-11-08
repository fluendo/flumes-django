from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class FlumeDjangoAppConfig(AppConfig):
    name = "flume_django"

    def ready(self):
        # Checking settings
        if "flume" not in settings.DATABASES:
            raise ImproperlyConfigured("Missing 'flume' database")
        if "flume_django.router.Router" not in settings.DATABASE_ROUTERS:
            raise ImproperlyConfigured("Missing 'flume_django.router.Router' router")
