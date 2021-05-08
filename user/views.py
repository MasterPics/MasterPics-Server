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




# ----------------------new-------------------------------
from .forms import SignupForm, LoginForm, ProfileModifyForm, LocalPasswordChangeForm
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
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

# TODO : logout 페이지 존재하면 GET방식 살려두고 존재하지 않으면 삭제
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('core:main_list')
    elif request.method == 'GET':
        return redirect('core:main_list')


# ----mypage 관련----
# TODO : 현재는 모든 유저가 자신의 프로필만 볼 수 있게 되어있음 -> 다른 사람의 프로필도 볼 수 있게 고치기
#         -> 파라미터에 user_identifier 추가, profile_owner 바꾸기
def profile_portfolio(request):
    profile_owner = request.user
    portfolios = profile_owner.portfolios.all()
    portfolio_count = profile_owner.portfolios.count()
    contact_count = profile_owner.contacts.count()

    ctx = {
        'profile_owner': profile_owner,
        'portfolios': portfolios,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/profile_portfolio.html', ctx)

def profile_post_contact(request):
    profile_owner = request.user
    contacts = profile_owner.contacts.all()
    portfolio_count = profile_owner.portfolios.count()
    contact_count = profile_owner.contacts.count()

    ctx = {
        'profile_owner': profile_owner,
        'contacts': contacts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/profile_post_contact.html', ctx)

# portfolio app > participants 먼저 구현해야 실행 가능
def profile_post_tagged(request):
    profile_owner = request.user
    taggeds = profile_owner.participants.all()      # profile_owner가 태그된 participant 객체들
    tagged_posts = []       # profile_owner가 태그된 portfolio 객체들
    for tagged in taggeds:
        tagged_posts.append(tagged.portfolio)

    portfolio_count = profile_owner.portfolios.count()
    contact_count = profile_owner.contacts.count()

    ctx = {
        'profile_owner': profile_owner,
        'tagged_posts': tagged_posts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/profile_post_tagged.html', ctx)

# TODO : 모델관련 회의 후 재구성 필요
# 이름 북마크로 바꾸고 싶다... 근데 다른데서 save로 다 해놨겠지..?ㅠㅠ
def profile_save(request):
    profile_owner = request.user
    
    # informations = Information.objects.filter(save_users=profile_owner)
    # print(informations)

    saved_informations = profile_owner.save_users.all()      # profile_owner가 save한 information 객체들
    print(saved_informations)
    
    saved_posts = []        # profile_owner가 save한 portfolio 객체들
    for info in saved_informations:
        saved_posts.append(PortfolioInformation.objects.filter(information=info).portfolio.title)
    print(saved_posts)

    saved_posts2 = []        # profile_owner가 save한 portfolio 객체들
    for info in saved_informations:
        saved_posts2.append(info.portfolioInformation_set.all())
    print(saved_posts)

    portfolio_count = profile_owner.portfolios.count()
    contact_count = profile_owner.contacts.count()

    ctx = {
        'profile_owner': profile_owner,
        # 'tagged_posts': tagged_posts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/profile_post_tagged.html', ctx)


# ----profile 관련----
def profile_modify(request):
    if request.method == 'POST':
        form = ProfileModifyForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile:profile_portfolio')
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

# TODO : 자동 로그아웃 할지 말지
# TODO : 기존과 같은 비밀번호로 바꿔도 바뀜...
def password_modify(request):
    if request.method == 'POST':
        form = LocalPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)     # 자동 로그아웃X
            return redirect('profile:profile_portfolio')
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