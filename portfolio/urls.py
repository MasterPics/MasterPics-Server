from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
     path('',
         view=views.portfolio_list, name='portfolio_list'),
     path('<int:pk>/', view=views.portfolio_detail,
         name='portfolio_detail'),
     path('<int:pk>/delete/',
         view=views.portfolio_delete, name='portfolio_delete'),
     path('<int:pk>/update/',
         view=views.portfolio_update, name='portfolio_update'),
     path('create/', view=views.portfolio_create, name='portfolio_create'),
     path('like/', view=views.portfolio_like,
         name='portfolio_like'),
     #save to bookmark
     path('save/', view=views.portfolio_save,
         name='portfolio_save'),
]
