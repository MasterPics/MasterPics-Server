from django.contrib import admin
from .models import *


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['user', 'title']

@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ['id', 'portfolio', 'participant']
    list_display_links = ['portfolio', 'participant']