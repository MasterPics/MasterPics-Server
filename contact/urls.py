from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', view=views.contact_list, name='contact_list'),
    path('map/', view=views.contact_map, name='contact_map'),
    path('detail/<int:pk>/',
         view=views.contact_detail, name='contact_detail'),
    path('<int:pk>/comment_create/',
         view=views.contact_comment_create, name='contact_comment_create'),
    path('<int:pk>/comment_delete/',
         view=views.contact_comment_delete, name='contact_comment_delete'),
    path('<int:pk>/delete/',
         view=views.contact_delete, name='contact_delete'),
    path('<int:pk>/update/',
         view=views.contact_update, name='contact_update'),
    path('create/', view=views.contact_create, name='contact_create'),
    path('save/', views.contact_save, name='contact_save'),
]
