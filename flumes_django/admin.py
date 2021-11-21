import os

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .forms import UploadFileForm
from .models import Audio, Container, Field, File, Info, Meta, Stream, Subtitle, Video


class MetaAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "root")

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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
            "admin/flumes_django/info/streams.html", {"children": children}
        )
        return content

    streams.allow_tags = True

    class Media:
        css = {"all": ("admin/flumes_django/common/topology.css",)}


class FieldInlineAdmin(admin.TabularInline):
    model = Field
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StreamAdmin(admin.ModelAdmin):
    inlines = [
        FieldInlineAdmin,
    ]

    def get_list_display(self, request):
        return (
            "id",
            "type",
            "media_type",
        )

    def get_readonly_fields(self, request, obj=None):
        return ("children",)

    def get_fieldsets(self, request, obj=None):
        # Same fields as list without it
        fields = list(self.get_list_display(request))
        fields.remove("id")
        fields = tuple(fields)
        return (
            (
                None,
                {"fields": fields},
            ),
            (
                "Topology",
                {
                    "fields": ("children",),
                },
            ),
        )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def children(self, obj):
        content = render_to_string(
            "admin/flumes_django/stream/children.html", {"root": obj}
        )
        return content

    children.allow_tags = True

    class Media:
        css = {"all": ("admin/flumes_django/common/topology.css",)}


class ContainerAdmin(StreamAdmin):
    pass


class VideoAdmin(StreamAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        readonly_fields += ("framerate", "par")
        return readonly_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display += (
            "bitrate",
            "max_bitrate",
            "depth",
            "framerate",
            "width",
            "height",
            "par",
            "is_image",
            "is_interlaced",
        )
        return list_display

    def par(self, obj):
        return "{}/{}".format(obj.par_num, obj.par_denom)

    def framerate(self, obj):
        return "{}/{}".format(obj.framerate_num, obj.framerate_denom)


class AudioAdmin(StreamAdmin):
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display += (
            "bitrate",
            "max_bitrate",
            "depth",
            "language",
            "channel_mask",
            "channels",
            "sample_rate",
        )
        return list_display


class SubtitleAdmin(StreamAdmin):
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display += ("language",)
        return list_display


class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
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
                name="flumes_django_file_upload",
            ),
        ]
        return urls + base_urls

    def upload(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                meta = Meta.objects.all()[0]
                # Upload the file to the Flume storage
                f = request.FILES["file"]
                name = os.path.join(meta.root, f.name)
                with open(name, "wb+") as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                return HttpResponseRedirect(
                    reverse("admin:flumes_django_file_changelist")
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
                request, "admin/flumes_django/file/upload.html", context
            )


admin.site.register(Meta, MetaAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Subtitle, SubtitleAdmin)
admin.site.register(Container, ContainerAdmin)
