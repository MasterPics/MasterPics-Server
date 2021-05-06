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


@login_required
def profile_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "탈퇴되었습니다.")
        return redirect('myApp:main_list')
    else:
        ctx = {'user': user}
        return render(request, 'profile/profile_delete.html', context=ctx)


@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print("form.is_valid")

            # user = form.save()
            # if user.image:
            #     user.image = request.FILES.get('image')
            # return redirect('myApp:profile_detail', user.id)
            user = form.save()
            user.image = request.FILES.get('image')

            return redirect('profile_detail', user.id)

    else:
        form = ProfileForm(instance=user)
        ctx = {'form': form}
        return render(request, 'profile/profile_update.html', ctx)


@login_required
def profile_update_password(request, pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/profile_update_password.html', {
        'form': form
    })


def profile_create(request):
    # if request.user.is_authenticated:
    #     return redirect('myApp:profile_detail')

    if request.method == 'POST':
        signup_form = ProfileForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            user.image = request.FILES['image']

            # automatic login
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')

            return redirect('profile:profile_detail', user.id)

    else:
        signup_form = ProfileForm()

    return render(request, 'profile/profile_create.html', {'form': signup_form})


@login_required
def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user=request.user
    ctx = {'user': user,'request_user':request_user, }
    return render(request, 'profile/profile_detail.html', context=ctx)


@login_required
def profile_detail_posts(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user=request.user

    category = request.GET.get('category', 'contact')  # CATEGORY
    # sort = request.GET.get('sort', 'recent')  # SORT
    # search = request.GET.get('search', '')  # SEARCH

    # CATEGORY
    if category == 'contact':
        posts = user.contacts.all()

    elif category == 'portfolio':
        posts = user.portfolios.all()

    # SORT

    # SEARCH

    # infinite scroll

    ctx = {
        'user': user,
        'posts': posts,
        'category': category,
    }
    return render(request, 'profile/profile_detail_posts.html', context=ctx)


@login_required
def profile_detail_saves(request, pk):
    user = get_object_or_404(User, pk=pk)
    request_user=request.user

    category = request.GET.get('category', 'contact')  # CATEGORY
    # sort = request.GET.get('sort', 'recent')  # SORT
    search = request.GET.get('search', '')  # SEARCH

    # CATEGORY
    if category == 'contact':
        posts = Contact.objects.all()
    elif category == 'portfolio':
        posts = Portfolio.objects.all()

    ctx = {
        'user': user,
        'posts': posts,
        'category': category,
        'request_user':request_user,
    }
    return render(request, 'profile/profile_detail_saves.html', context=ctx)


@login_required
def post_create(request):
    if request.method == 'POST':
        messages.success(request, "create your post!")
    else:
        ctx = {}
        return render(request, 'profile/post_create.html', context=ctx)



# social sign up 시 -> 추가 정보 입력받기
def social_signup(request):
    if request.method == "POST" :
        form = SocialSignUpForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect("profile:profile_detail", pk = user.pk)
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'profile/social_signup.html', ctx)
    # 현재 유저가 약관 동의를 하지 않았을 경우 (== 추가 정보를 입력하지 않았을 경우)
    elif request.method == 'GET' and (request.user.is_ToS == False):
        form = SocialSignUpForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/social_signup.html', ctx)
    elif request.method == 'GET':
        return redirect("profile:profile_detail", pk = request.user.pk)