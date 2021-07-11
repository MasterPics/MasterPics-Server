from django.urls import path
from . import views

app_name = 'reference'

urlpatterns = [
    path('', view=views.reference_list, name='reference_list'),
    path('local/<slug:tag>/', view=views.reference_local_detail, name='reference_local_detail'),
]