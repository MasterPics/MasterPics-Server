from django.urls import path
from . import views

app_name = 'reference'

urlpatterns = [
    path('local/', view=views.local_list, name='local_list'),
    path('local/<slug:tag>/', view=views.local_detail, name='local_detail'),
]
