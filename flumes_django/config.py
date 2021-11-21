from flumes.config import Config


class FlumesDjangoConfig(Config):
    def get_django_database_engine(self):
        driver = self.get_database_driver()
        if "postgresql" in driver:
            return "django.db.backends.postgresql_psycopg2"
        elif "mysql" in driver:
            return "django.db.backends.mysql"
        elif "sqlite" in driver:
            return "django.db.backends.sqlite3"
        else:
            return None
