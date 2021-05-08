from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('<int:pk>/', view=views.profile_detail, name='profile_detail'),
    path('<int:pk>/posts/',
         view=views.profile_detail_posts, name='profile_detail_posts'),
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
#     ------------------------new------------------------------
     path('local_signup/', view=views.local_signup, name='local_signup'),
     path('login/', view=views.login, name='login'),
     path('logout/', view=views.logout, name='logout'),
     path('profile_portfolio/', view=views.profile_portfolio, name='profile_portfolio'),
     path('profile_post_contact/', view=views.profile_post_contact, name='profile_post_contact'),
     path('profile_post_tagged/', view=views.profile_post_tagged, name='profile_post_tagged'),
     path('profile_save/', view=views.profile_save, name='profile_save'),
     path('profile_modify/', view=views.profile_modify, name='profile_modify'),
     path('password_modify/', view=views.password_modify, name='password_modify'),
     path('social_user_more_info/', view=views.social_user_more_info, name='social_user_more_info'),
]
