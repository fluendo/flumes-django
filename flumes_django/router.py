class Router(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "flumes_django":
            return "flumes"
        return None

    def db_for_write(self, model, **hints):
        # We don't allow to write, maybe later, but not now.
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "flumes_django":
            return False
        return None
