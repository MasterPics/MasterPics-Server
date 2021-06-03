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
from portfolio.models import Portfolio, PortfolioInformation
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

# mypage / 포트폴리오 / 나의 포트폴리오
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

# mypage / 포트폴리오 / 태그된 목록
def mypage_portfolio_tagged(request):
    mypage_owner = request.user
    taggeds = mypage_owner.participants.all()      # mypage_owner 태그된 participant 객체들
    tagged_portfolios = []       # mypage_owner 태그된 portfolio 객체들
    for tagged in taggeds:
        tagged_portfolios.append(tagged.portfolio)

    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'tagged_portfolios': tagged_portfolios,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_portfolio_tagged.html', ctx)

# mypage / 게시글 / 컨택트
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

# mypage / 게시글 / 플레이스
def mypage_post_place(request):
    mypage_owner = request.user
    places = mypage_owner.places.all()
    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'places': places,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_post_place.html', ctx)

from portfolio.models import PortfolioInformation
# mypage / 저장 목록 / 포트폴리오
def mypage_bookmark_portfolio(request):
    mypage_owner = request.user
    # bookmarked_informations = mypage_owner.save_users.all()      # mypage_owner가 bookmark한 information 객체들
    # bookmarked_portfolios = []        # mypage_owner bookmark한 portfolio 객체들
    # for info in bookmarked_informations:
    #     bookmarked_portfolios.append(info.portfolioInformations.portfolio)  # info가 portfolioInformation이 아닌 다른 곳(contactInformation, placeInformation)에
    #                                                                         # 연결되어있으면 오류 발생. portfolioInformations가 없다고 나옴
    
    # TODO : manyTomany 쿼리 필터 공부하기 -> 코드 효율적으로 수정 필요
    bookmarked_informations = Information.objects.filter(save_users = mypage_owner)     # mypage_owner가 bookmark한 information 객체들
    portfolioInformations = PortfolioInformation.objects.all()                          # 모든 portfolioInformation 객체들
    bookmarked_portfolios = []                                                          # mypage_owner가 bookmark한 portfolio 객체들
    for portfolioInformation in portfolioInformations:
        for information in bookmarked_informations:
            if portfolioInformation.information == information:
                bookmarked_portfolios.append(portfolioInformation.portfolio)

    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'bookmarked_portfolios': bookmarked_portfolios,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_bookmark_portfolio.html', ctx)


from contact.models import ContactInformation
# mypage / 저장 목록 / 컨택트
def mypage_bookmark_contact(request):
    mypage_owner = request.user
    # bookmarked_informations = mypage_owner.save_users.all()
    # bookmarked_contacts = []
    # for info in bookmarked_informations:
    #     bookmarked_contacts.append(info.contactInformations.contact)

    # TODO : manyTomany 쿼리 필터 공부하기 -> 코드 효율적으로 수정 필요
    bookmarked_informations = Information.objects.filter(save_users = mypage_owner)     # mypage_owner가 bookmark한 information 객체들
    contactInformations = ContactInformation.objects.all()                          # 모든 portfolioInformation 객체들
    bookmarked_contacts = []                                                          # mypage_owner가 bookmark한 portfolio 객체들
    for contactInformation in contactInformations:
        for information in bookmarked_informations:
            if contactInformation.information == information:
                bookmarked_contacts.append(contactInformation.contact)
    
    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'bookmarked_contacts': bookmarked_contacts,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_bookmark_contact.html', ctx)
    

from place.models import PlaceInformation
# mypage / 저장 목록 / 플레이스
def mypage_bookmark_place(request):
    mypage_owner = request.user
    # bookmarked_informations = mypage_owner.save_users.all()
    # bookmarked_contacts = []
    # for info in bookmarked_informations:
    #     bookmarked_contacts.append(info.contactInformations.contact)

    # TODO : manyTomany 쿼리 필터 공부하기 -> 코드 효율적으로 수정 필요
    bookmarked_informations = Information.objects.filter(save_users = mypage_owner)     # mypage_owner가 bookmark한 information 객체들
    placeInformations = PlaceInformation.objects.all()                          # 모든 portfolioInformation 객체들
    bookmarked_places = []                                                          # mypage_owner가 bookmark한 portfolio 객체들
    for placeInformation in placeInformations:
        for information in bookmarked_informations:
            if placeInformation.information == information:
                bookmarked_places.append(placeInformation.place)
    
    portfolio_count = mypage_owner.portfolios.count()
    contact_count = mypage_owner.contacts.count()

    ctx = {
        'mypage_owner': mypage_owner,
        'bookmarked_places': bookmarked_places,
        'portfolio_count': portfolio_count,
        'contact_count': contact_count,
    }

    return render(request, 'profile/mypage_bookmark_place.html', ctx)
 

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