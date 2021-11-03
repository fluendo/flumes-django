from django.db import models

from flume_django.managers import StreamManager


class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    path = models.CharField(max_length=512)
    mtime = models.DateTimeField()

    class Meta:
        db_table = "files"
        managed = False


class Info(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    duration = models.IntegerField()
    seekable = models.BooleanField()
    live = models.BooleanField()
    audio_streams = models.IntegerField()
    video_streams = models.IntegerField()
    subtitle_streams = models.IntegerField()

    class Meta:
        db_table = "infos"
        managed = False


class Stream(models.Model):
    class StreamType(models.TextChoices):
        VIDEO = "video", "Video"
        AUDIO = "audio", "Audio"
        SUBTITLE = "subtitle", "Subtitle"
        CONTAINER = "container", "Container"

    id = models.AutoField(primary_key=True)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", related_name="children", on_delete=models.CASCADE
    )
    media_type = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=StreamType.choices)
    # Common fields for a single table inheritance
    bitrate = models.IntegerField()
    max_bitrate = models.IntegerField()
    depth = models.IntegerField()
    language = models.CharField(max_length=256)
    # Video fields
    framerate_denom = models.IntegerField()
    framerate_num = models.IntegerField()
    height = models.IntegerField()
    par_denom = models.IntegerField()
    par_num = models.IntegerField()
    width = models.IntegerField()
    is_image = models.BooleanField()
    is_interlaced = models.BooleanField()
    # Audio fields
    channel_mask = models.IntegerField()
    channels = models.IntegerField()
    sample_rate = models.IntegerField()
    # Subtitle fields
    # Container fields
    class Meta:
        db_table = "streams"
        managed = False


class Video(Stream):
    objects = StreamManager()

    class Meta:
        proxy = True


class Audio(Stream):
    objects = StreamManager()

    class Meta:
        proxy = True


class Subtitle(Stream):
    objects = StreamManager()

    class Meta:
        proxy = True


class Container(Stream):
    objects = StreamManager()

    class Meta:
        proxy = True


class Field(models.Model):
    id = models.AutoField(primary_key=True)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=1024)

    class Meta:
        db_table = "fields"
        managed = False
