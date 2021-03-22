from django.urls import path
from . import views

app_name = 'reference'

urlpatterns = [
    path('local/', view=views.reference_local_list, name='reference_local_list'),
    path('local/<slug:tag>/', view=views.reference_local_detail, name='reference_local_detail'),
]