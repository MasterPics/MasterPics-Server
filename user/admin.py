from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'email']
    list_display_links = ['user_id', 'username', 'email']