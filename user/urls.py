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

     #TODO 다른 사람꺼 보기
     path('others/<str:pk>', view=views.others_profile, name='others_profile'),

     # smpt
     path('smtp_sending_success/', view=views.smtp_sending_success, name='smtp_sending_success'),
     path('smtp_auth/<str:uid64>/<str:token>/', view=views.smtp_auth, name='smtp_auth'),

     # 비밀번호 인증관련
     path('recovery/pw/', view=views.recovery_pw, name='recovery_pw'),
     path('recovery/pw/find/', view=views.recovery_pw_send_email, name='ajax_pw'),
     path('recovery/pw/auth/', view=views.recovery_pw_auth_confirm, name='recovery_auth'),
     path('recovery/pw/reset/', view=views.recovery_pw_reset, name='recovery_pw_reset'),

]
