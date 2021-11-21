from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class FlumesDjangoAppConfig(AppConfig):
    name = "flumes_django"

    def ready(self):
        # Checking settings
        if "flumes" not in settings.DATABASES:
            raise ImproperlyConfigured("Missing 'flumes' database")
        if "flumes_django.router.Router" not in settings.DATABASE_ROUTERS:
            raise ImproperlyConfigured("Missing 'flumes_django.router.Router' router")
