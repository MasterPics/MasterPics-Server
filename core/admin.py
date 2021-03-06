from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'lat', 'lon']
    list_display_links = ['id', 'address', 'lat', 'lon']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'writer', 'created_at']
    list_display_links = ['id', 'writer', 'created_at']


@admin.register(PostBookmark)
class PostBookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    list_display_links = ['id', 'user', 'post']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'created_at']
    list_display_links = ['image', 'created_at']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'post']
    list_display_links = ['image', 'post']
