from django.contrib import admin
from .models import *


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass
