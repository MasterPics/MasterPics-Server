from django.contrib import admin
from .models import *


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']


