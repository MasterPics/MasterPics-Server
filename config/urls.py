"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from rest_framework import routers
from contact.views import ContactViewsets
from core.views import LocationViewsets

router = routers.DefaultRouter()
router.register("contact", ContactViewsets)
router.register("location", LocationViewsets)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("api/auth/", include("knox.urls")),
    path("api/", include(router.urls)),
    #
    # path('place/', include('place.urls')),
    path("profile/", include("user.urls")),
    # path("contact/", include("contact.urls")),
    # path('portfolio/', include('portfolio.urls')),
    # path('reference/', include('reference.urls')),
    # path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
