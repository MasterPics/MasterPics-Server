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
     path('mypage/portfolio/', view=views.mypage_portfolio, name='mypage_portfolio'),
     path('mypage/portfolio/tagged/', view=views.mypage_portfolio_tagged, name='mypage_portfolio_tagged'),
     path('mypage/post/contact/', view=views.mypage_post_contact, name='mypage_post_contact'),
     path('mypage/post/place/', view=views.mypage_post_place, name='mypage_post_place'),
     path('mypage/bookmark/portfolio/', view=views.mypage_bookmark_portfolio, name='mypage_bookmark_portfolio'),
     path('mypage/bookmark/contact/', view=views.mypage_bookmark_contact, name='mypage_bookmark_contact'),
     path('mypage/bookmark/place/', view=views.mypage_bookmark_place, name='mypage_bookmark_place'),
     path('profile/modify/', view=views.profile_modify, name='profile_modify'),
     path('password/change/', view=views.password_change, name='password_change'),
     path('social_user_more_info/', view=views.social_user_more_info, name='social_user_more_info'),

     #TODO 다른 사람꺼 보기
     path('others/<str:pk>', view=views.others_mypage, name='others_mypage'),

     # smpt
     path('smtp_sending_success/', view=views.smtp_sending_success, name='smtp_sending_success'),
     path('local_signup_auth/<str:uid64>/<str:token>/', view=views.local_signup_auth, name='local_signup_auth'),

     # ecovery password
     path('recovery/pw/', view=views.recovery_pw, name='recovery_pw'),
     path('recovery/pw/send_email/', view=views.recovery_pw_send_email, name='recovery_pw_send_email'),
     path('recovery/pw/auth/', view=views.recovery_pw_auth, name='recovery_pw_auth'),
     path('recovery/pw/reset/', view=views.recovery_pw_reset, name='recovery_pw_reset'),

     # ToS
     path('terms_of_service_use/', view=views.terms_of_service_use, name='terms_of_service_use'),
     path('personal_info_policy/', view=views.personal_info_policy, name='personal_info_policy')
]
