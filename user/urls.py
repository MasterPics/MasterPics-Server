from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
#     ------------------------new------------------------------
     path('local_signup/', view=views.local_signup, name='local_signup'),
     path('login/', view=views.login, name='login'),
     path('logout/', view=views.logout, name='logout'),
     path('withdrawal/', view=views.withdrawal, name='withdrawal'),
     path('mypage/', view=views.mypage, name='mypage'),
     path('mypage_portfolio/', view=views.mypage_portfolio, name='mypage_portfolio'),
     path('mypage_post_contact/', view=views.mypage_post_contact, name='mypage_post_contact'),
     path('mypage_post_tagged/', view=views.mypage_post_tagged, name='mypage_post_tagged'),
     path('mypage_bookmark/', view=views.mypage_bookmark, name='mypage_bookmark'),
     path('profile_modify/', view=views.profile_modify, name='profile_modify'),
     path('password_modify/', view=views.password_modify, name='password_modify'),
     path('social_user_more_info/', view=views.social_user_more_info, name='social_user_more_info'),

     #TODO 다른 사람꺼 보기
     path('others/<str:pk>', view=views.others_profile, name='others_profile'),
]
