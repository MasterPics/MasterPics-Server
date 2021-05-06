from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
     #그냥 detail
     path('<int:pk>/', view=views.profile_detail, name='profile_detail'),
     #내가 올린 글 contact랑 portfolio 다 보여 주는 것
     path('<int:pk>/list/',
         view=views.profile_detail_list, name='profile_detail_list'),
     #내가 북마크 한 것들을 보여줌
     path('<int:pk>/saves/',
         view=views.profile_detail_saves, name='profile_detail_saves'),
     path('<int:pk>/delete/',
         view=views.profile_delete, name='profile_delete'),
     path('<int:pk>/update/',
         view=views.profile_update, name='profile_update'),
     path('<int:pk>/profile_update_password/',
         view=views.profile_update_password, name='profile_update_password'),
     path('create/', view=views.profile_create, name='profile_create'),
     path('post/create/', view=views.post_create, name='post_create'),
]
