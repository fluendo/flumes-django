import os

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import path, reverse

from flume_django.config import Config
from flume_django.forms import UploadFileForm
from flume_django.models import (
    Audio,
    Container,
    Field,
    File,
    Info,
    Stream,
    Subtitle,
    Video,
)


class InfoInlineAdmin(admin.StackedInline):
    model = Info
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "duration",
                    "seekable",
                    "live",
                    "audio_streams",
                    "video_streams",
                    "subtitle_streams",
                ),
            },
        ),
        (
            "Topology",
            {
                "fields": ("streams",),
            },
        ),
    )
    readonly_fields = ("streams",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def streams(self, obj):
        children = Stream.objects.filter(info=obj, parent=None)
        content = render_to_string(
            "admin/flume_django/info/topology.html", {"children": children}
        )
        return content

    streams.allow_tags = True

    class Media:
        css = {"all": ("admin/flume_django/info/topology.css",)}


class FieldAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FileAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [
        InfoInlineAdmin,
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        base_urls = super().get_urls()
        urls = [
            path(
                "upload/",
                self.admin_site.admin_view(self.upload),
                name="flume_django_file_upload",
            ),
        ]
        return urls + base_urls

    def upload(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                # Upload the file to the Flume storage
                config = Config()
                f = request.FILES["file"]
                name = os.path.join(config.get_media_files_directory(), f.name)
                with open(name, "wb+") as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                return HttpResponseRedirect(
                    reverse("admin:flume_django_file_changelist")
                )
        else:
            form = UploadFileForm()
            opts = self.model._meta
            context = {
                **self.admin_site.each_context(request),
                "opts": opts,
                "has_view_permission": self.has_view_permission(request),
                "form": form,
            }
            return TemplateResponse(
                request, "admin/flume_django/file/upload.html", context
            )


admin.site.register(File, FileAdmin)
admin.site.register(Info)
admin.site.register(Stream)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Subtitle)
admin.site.register(Container)
admin.site.register(Field, FieldAdmin)
