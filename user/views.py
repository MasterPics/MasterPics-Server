from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from .forms import *
from .models import *
# from core.utils import *


# ----------------------new-------------------------------
from .forms import SignupForm, LoginForm, ProfileModifyForm, LocalPasswordChangeForm, SocialUserInfoForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from portfolio.models import PortfolioInformation
from core.models import Information
from django.contrib.auth import update_session_auth_hash

# ----login 관련----
def local_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:main_list')
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'profile/local_signup.html', ctx)
    elif request.method == 'GET':
        form = SignupForm()
        ctx = {
            'form': form,
        }
        return render(request, 'profile/local_signup.html', ctx)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(user_id=user_id, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('core:main_list')
        else:
            ctx = {
                'form': form,
                'error': '아이디 혹은 비밀번호가 올바르지 않습니다.'
            }
            return render(request, 'profile/login.html', ctx)
    elif request.method == 'GET':
        form = LoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'profile/login.html', ctx)

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('core:main_list')

# social sign up 시 -> 추가 정보 입력받기
def social_user_more_info(request):
    if request.method == 'POST':
        form = SocialUserInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.is_social = True
            form.save()
            return redirect('profile:mypage')
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'profile/social_user_more_info.html', ctx)
    # 현재 유저가 약관 동의를 하지 않았을 경우 (== 추가 정보를 입력하지 않았을 경우)
    if request.method == 'GET' and (request.user.is_ToS == False):
        form = SocialUserInfoForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/social_user_more_info.html', ctx)
    elif request.method == 'GET':
        return redirect('profile:mypage')

def withdrawal(request):
    if request.method == 'POST':
        request.user.delete()
        # TODO : 추후 모달창으로 / messages.success(request, "탈퇴되었습니다.")
        return redirect('core:main_list')
    # TODO : 추후 모달창으로
    else:
        return render(request, 'profile/withdrawal.html')


# ----mypage 관련----
# TODO : 현재는 모든 유저가 자신의 프로필만 볼 수 있게 되어있음 -> 다른 사람의 프로필도 볼 수 있게 고치기
#         -> 파라미터에 user_identifier 추가, mypage_owner 바꾸기
def mypage(request):
    return redirect('profile:mypage_portfolio')

def mypage_portfolio(request):
    mypage_owner = request.user
    portfolios = mypage_owner.portfolios.all()
    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'portfolios': portfolios,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_portfolio.html', ctx)

def mypage_post_contact(request):
    mypage_owner = request.user
    contacts = mypage_owner.contacts.all()
    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'contacts': contacts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_post_contact.html', ctx)

def mypage_post_tagged(request):
    mypage_owner = request.user
    taggeds = mypage_owner.participants.all()      # mypage_owner 태그된 participant 객체들
    tagged_posts = []       # mypage_owner 태그된 portfolio 객체들
    for tagged in taggeds:
        tagged_posts.append(tagged.portfolio)

    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'tagged_posts': tagged_posts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_post_tagged.html', ctx)

def mypage_bookmark(request):
    mypage_owner = request.user
    saved_informations = mypage_owner.save_users.all()      # mypage_owner bookmark한 information 객체들
    saved_posts = []        # mypage_owner bookmark한 portfolio 객체들
    for info in saved_informations:
        saved_posts.append(info.portfolioInformation_set.portfolio)

    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'saved_posts': saved_posts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_bookmark.html', ctx)


# ----profile 관련----
def profile_modify(request):
    if request.method == 'POST':
        form = ProfileModifyForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile:mypage')
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'profile/profile_modify.html', ctx)
    elif request.method == 'GET':
        form = ProfileModifyForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/profile_modify.html', ctx)

# TODO : 기존과 같은 비밀번호로 바꿔도 바뀜...
def password_modify(request):
    if request.method == 'POST':
        form = LocalPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # update_session_auth_hash(request, request.user)     # 자동 로그아웃X
            return redirect('profile:login')
        else:
            ctx = {
                'form': form,
            }
            return render(request, 'profile/password_modify.html', ctx)
    elif request.method == 'GET':
        form = LocalPasswordChangeForm(request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/password_modify.html', ctx)