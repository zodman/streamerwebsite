from django.contrib import admin
from .models import *



admin.site.register(Media)

class EntryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "media", "episode", "season","get_resources")

    def get_resources(self, obj):
        return obj.resources.count()

admin.site.register(Entry, EntryAdmin)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ("entry", "quality", "source")

admin.site.register(Resource, ResourceAdmin)
