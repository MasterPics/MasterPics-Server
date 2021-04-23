from django.contrib import admin
from .models import Location, Tag


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "lon",
        "lat",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("tag",)
