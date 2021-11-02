from django.apps import AppConfig
from flume.config import Config, ConfigError


class FlumeDjangoAppConfig(AppConfig):
    name = "flume_django"

    def ready(self):
        try:
            config = Config()
        except ConfigError:
            print("No configuration, checking settings")
        # Get the flume configuration
        # Create a new live database
        # Install the router if needed
        print("Check the flume database")
        print("Check the flume router")
