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
     path('password_change/', view=views.password_change, name='password_change'),
     path('social_user_more_info/', view=views.social_user_more_info, name='social_user_more_info'),

     #TODO 다른 사람꺼 보기
     path('others/<str:pk>', view=views.others_profile, name='others_profile'),

     # smpt
     path('smtp_sending_success/', view=views.smtp_sending_success, name='smtp_sending_success'),
     path('local_signup_auth/<str:uid64>/<str:token>/', view=views.local_signup_auth, name='local_signup_auth'),

     # ecovery password
     path('recovery/pw/', view=views.recovery_pw, name='recovery_pw'),
     path('recovery/pw/find/', view=views.recovery_pw_send_email, name='recovery_pw_send_email'),
     path('recovery/pw/auth/', view=views.recovery_pw_auth, name='recovery_pw_auth'),
     path('recovery/pw/reset/', view=views.recovery_pw_reset, name='recovery_pw_reset'),

]
