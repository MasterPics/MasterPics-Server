from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', view=views.main_list, name='main_list'),
]