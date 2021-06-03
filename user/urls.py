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
     path('mypage_portfolio_tagged/', view=views.mypage_portfolio_tagged, name='mypage_portfolio_tagged'),
     path('mypage_post_contact/', view=views.mypage_post_contact, name='mypage_post_contact'),
     path('mypage_post_place/', view=views.mypage_post_place, name='mypage_post_place'),
     path('mypage_bookmark_portfolio/', view=views.mypage_bookmark_portfolio, name='mypage_bookmark_portfolio'),
     path('mypage_bookmark_contact/', view=views.mypage_bookmark_contact, name='mypage_bookmark_contact'),
     path('mypage_bookmark_place/', view=views.mypage_bookmark_place, name='mypage_bookmark_place'),
     path('profile_modify/', view=views.profile_modify, name='profile_modify'),
     path('password_modify/', view=views.password_modify, name='password_modify'),
     path('social_user_more_info/', view=views.social_user_more_info, name='social_user_more_info'),
]
