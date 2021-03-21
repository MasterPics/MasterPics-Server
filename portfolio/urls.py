from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('portfolio/',
         view=views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', view=views.portfolio_detail,
         name='portfolio_detail'),
    path('portfolio/<int:pk>/delete/',
         view=views.portfolio_delete, name='portfolio_delete'),
    path('portfolio/<int:pk>/update/',
         view=views.portfolio_update, name='portfolio_update'),
    path('portfolio/create/', view=views.portfolio_create, name='portfolio_create'),
    path('portfolio/like/', view=views.portfolio_like,
         name='portfolio_like'),
    path('portfolio/save/', view=views.portfolio_save,
         name='portfolio_save'),
]
