from django.contrib import admin
from .models import *

# from .forms import ContactForm

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # form = ContactForm
    list_display = ['id', 'user', 'title']
    list_display_links = ['title']


