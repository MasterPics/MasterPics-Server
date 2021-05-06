from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Images)
class PortfolioAdmin(admin.ModelAdmin):
    pass


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


# @admin.register(ViewCount)
# class ViewCountAdmin(admin.ModelAdmin):
#     pass

class Images(admin.TabularInline):
    model = Images


class PortfolioAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        for img in request.FILES.getlist('photos'):
            obj.productimage_set.create(image_url=img)
