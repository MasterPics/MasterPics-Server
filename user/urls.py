from django.urls import path
from . import views

from user.views import RegistrationAPI, LoginView

app_name = "profile"

urlpatterns = [
    path("<int:pk>/", view=views.profile_detail, name="profile_detail"),
    path(
        "<int:pk>/posts/", view=views.profile_detail_posts, name="profile_detail_posts"
    ),
    path(
        "<int:pk>/saves/", view=views.profile_detail_saves, name="profile_detail_saves"
    ),
    path("<int:pk>/delete/", view=views.profile_delete, name="profile_delete"),
    path("<int:pk>/update/", view=views.profile_update, name="profile_update"),
    path(
        "<int:pk>/profile_update_password/",
        view=views.profile_update_password,
        name="profile_update_password",
    ),
    path("create/", view=views.profile_create, name="profile_create"),
    path("post/create/", view=views.post_create, name="post_create"),
    #
    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginView.as_view()),
]
