from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


# @admin.register(ViewCount)
# class ViewCountAdmin(admin.ModelAdmin):
#     pass
