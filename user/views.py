from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse
from .forms import *
from .models import *
from contact.models import Contact

from django.contrib.auth import login as auth_login
from core.utils import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
    ]

    def post(self, request, format=None):
        print(request)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


# django rest framefork
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from knox.models import AuthToken


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user),
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@login_required
def profile_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect("myApp:main_list")
    else:
        ctx = {"user": user}
        return render(request, "profile/profile_delete.html", context=ctx)


@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("form.is_valid")

            # user = form.save()
            # if user.image:
            #     user.image = request.FILES.get('image')
            # return redirect('myApp:profile_detail', user.id)
            user = form.save()
            user.image = request.FILES.get("image")

            return redirect("profile_detail", user.id)

    else:
        form = ProfileForm(instance=user)
        ctx = {"form": form}
        return render(request, "profile/profile_update.html", ctx)


@login_required
def profile_update_password(request, pk):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "profile/profile_update_password.html", {"form": form})


def profile_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == "POST":
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            user.image = request.FILES["image"]

            # automatic login
            auth_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )

            return redirect("profile:profile_detail", user.id)

    else:
        signup_form = ProfileForm()

    return render(request, "profile/profile_create.html", {"form": signup_form})


@login_required
def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user = request.user
    ctx = {
        "user": user,
        "request_user": request_user,
    }
    return render(request, "profile/profile_detail.html", context=ctx)


@login_required
def profile_detail_posts(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user = request.user

    category = request.GET.get("category", "contact")  # CATEGORY
    # sort = request.GET.get('sort', 'recent')  # SORT
    # search = request.GET.get('search', '')  # SEARCH

    # CATEGORY
    if category == "contact":
        posts = user.contacts.all()

    elif category == "portfolio":
        posts = user.portfolios.all()

    # SORT

    # SEARCH

    # infinite scroll

    ctx = {
        "user": user,
        "posts": posts,
        "category": category,
    }
    return render(request, "profile/profile_detail_posts.html", context=ctx)


@login_required
def profile_detail_saves(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user = request.user

    category = request.GET.get("category", "contact")  # CATEGORY
    # sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get("search", "")  # SEARCH

    # CATEGORY
    if category == "contact":
        posts = Contact.objects.all()
    elif category == "portfolio":
        posts = Portfolio.objects.all()

    ctx = {
        "user": user,
        "posts": posts,
        "category": category,
        "request_user": request_user,
    }
    return render(request, "profile/profile_detail_saves.html", context=ctx)


@login_required
def post_create(request):
    if request.method == "POST":
        messages.success(request, "create your post!")
    else:
        ctx = {}
        return render(request, "profile/post_create.html", context=ctx)
