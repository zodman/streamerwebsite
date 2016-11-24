from django.contrib import admin
from .models import *



admin.site.register(Media)

class EntryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "media", "episode", "season")

admin.site.register(Entry, EntryAdmin)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ("entry", "quality", "source")

admin.site.register(Resource, ResourceAdmin)

admin.site.register(MainMedia)
