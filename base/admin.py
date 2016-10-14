from django.contrib import admin
from .models import *



admin.site.register(Media)

class EntryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "media", "episode", "season")

admin.site.register(Entry, EntryAdmin)
admin.site.register(Resource)
