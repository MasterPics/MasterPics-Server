from django.contrib import admin
from .models import *

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title']
    list_display_links = ['user', 'title']

@admin.register(PortfolioComment)
class PortfolioCommentAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'comment']
    list_display_links = ['portfolio', 'comment']

@admin.register(PortfolioInformation)
class PortfolioInformationAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'information']
    list_display_links = ['portfolio', 'information']

@admin.register(PortfolioParticipant)
class PortfolioParticipantAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'participant']
    list_display_links = ['portfolio', 'participant']