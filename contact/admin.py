from django.contrib import admin
from .models import *

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']

@admin.register(ContactComment)
class ContactCommentAdmin(admin.ModelAdmin):
    list_display = ['contact', 'comment']
    list_display_links = ['contact', 'comment']

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['contact', 'information']
    list_display_links = ['contact', 'information']
