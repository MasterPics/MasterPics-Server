from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Images)
class PortfolioAdmin(admin.ModelAdmin):
    pass

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass

@admin.register(PortfolioComment)
class PortfolioCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(PortfolioInformation)
class PortfolioInformationAdmin(admin.ModelAdmin):
    pass


# @admin.register(ViewCount)
# class ViewCountAdmin(admin.ModelAdmin):
#     pass
