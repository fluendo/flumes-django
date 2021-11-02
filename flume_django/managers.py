from django.db import models


class StreamManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.__name__.lower())
