from django.contrib import admin
from .models import *


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']


@admin.register(PlaceComment)
class PlaceCommentAdmin(admin.ModelAdmin):
    list_display = ['place', 'comment']
    list_display_links = ['place', 'comment']


@admin.register(PlaceInformation)
class PlaceInformationAdmin(admin.ModelAdmin):
    list_display = ['place', 'information']
    list_display_links = ['place', 'information']


@admin.register(PlaceImages)
class PlaceImagesAdmin(admin.ModelAdmin):
    list_display = ['place', 'image']
    list_display_links = ['place', 'image']
