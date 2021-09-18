from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
from .forms import *
from .models import *
# from core.utils import *
import time
import hashlib

# ----------------------new-------------------------------
from .forms import SignupForm, LoginForm, ProfileModifyForm, LocalPasswordChangeForm, SocialUserInfoForm
from portfolio.models import Portfolio, Participants
from contact.models import Contact
from place.models import Place
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash

# ----------------------smtp-------------------------------
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .utils import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect

# ----recovery password 관련----
from .forms import RecoveryPwForm
from django.views.decorators.csrf import csrf_exempt
from .utils import email_auth_num
import json
from .forms import CustomSetPasswordForm

# ----------------------smtp-------------------------------
from .decorators import allowed_user, required_login, local_user


# ----login 관련----


@csrf_protect
def local_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            customer = form.save()

            # hash (add user_identifier)
            string = str(customer.pk + int(time.time()))
            encoded_string = string.encode()
            result = hashlib.sha256(encoded_string).hexdigest()
            customer.user_identifier = result
            form.save()

            # smtp
            send_mail(
                "[masterpic's]: {}님의 회원가입 인증메일 입니다.".format(customer.user_id),
                [customer.email],
                html=render_to_string('profile/local_signup_email.html', {
                    'user': customer,
                    'uid': urlsafe_base64_encode(force_bytes(customer.pk)).encode().decode(),
                    'domain': request.META['HTTP_HOST'],
                    'token': default_token_generator.make_token(customer),
                }),
            )

            request.session['smtp_auth'] = True

            return redirect('profile:smtp_sending_success')
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


def local_signup_auth(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        # messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('profile:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        # messages.success(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('profile:login')

    # messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('profile:login')


def smtp_sending_success(request):
    if not request.session.get('smtp_auth', False):
        raise PermissionDenied
    request.session['smtp_auth'] = False
    return render(request, 'profile/smtp_sending_success.html')


def login(request):
    # next_url
    next_url = request.GET.get("next")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(user_id=user_id, password=password)

        if user is not None:
            auth_login(request, user)

            # next_url
            if next_url:
                return redirect(next_url)
            return redirect('core:main_list')
        elif User.objects.filter(user_id=user_id) and not User.objects.filter(user_id=user_id)[0].is_active:
            ctx = {
                'form': form,
                'error': '회원가입 후 이메일 인증이 완료되지 않았습니다. 인증을 완료해주세요.'
            }
            return render(request, 'profile/login.html', ctx)
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

            customer = form.save()
            string = str(customer.pk + int(time.time()))
            encoded_string = string.encode()
            result = hashlib.sha256(encoded_string).hexdigest()
            customer.user_identifier = result

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
        return redirect('core:main_list')
    elif request.method == 'GET':
        return render(request, 'profile/withdrawal.html')


# ----mypage 관련----
@required_login
@allowed_user
def mypage(request):
    ctx = {
        'portfolios': request.user.portfolios.all(),
        'contacts' : request.user.contacts.all(),
    }

    return render(request, 'profile/mypage.html', ctx)


# TODO Superuser는 생성하면 hash값이 비어있음 -> 직접 입력해주거나 슈퍼 유저는 DB 관리용으로만 글을 써야함
def others_mypage(request, pk):
    profile_owner = get_object_or_404(User, user_identifier=pk)

    ctx = {
        'profile_owner': profile_owner,
        'portfolios': profile_owner.portfolios.all(),
        'contacts': profile_owner.contacts.all()
    }

    return render(request, 'profile/mypage_others.html', context=ctx)
    

# mypage / 포트폴리오 / 나의 포트폴리오
@csrf_exempt
def mypage_portfolio(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    portfolios_query = Portfolio.objects.filter(user=mypage_owner)
    portfolios = []
    for portfolio in portfolios_query:
        portfolios.append({
            'id': portfolio.id,
            'title': portfolio.title,
            'thumbnail_url': portfolio.thumbnail.image.url,
            'comment_count': portfolio.comments.count(),
            'view_count': portfolio.view_count,
            'like_count': portfolio.like_users.count(),
            'bookmark_count': portfolio.bookmark_users.count()
        })

    return JsonResponse({"portfolios": portfolios})
        

# mypage / 포트폴리오 / 태그된 목록
@csrf_exempt
def mypage_portfolio_tagged(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    tagged_portfolios_query = Portfolio.objects.filter(participants=mypage_owner)
    tagged_portfolios = []       # request.user 태그된 portfolio 객체들
    for portfolio in tagged_portfolios_query:
        tagged_portfolios.append({
            'id': portfolio.id,
            'title': portfolio.title,
            'thumbnail_url': portfolio.thumbnail.image.url,
            'comment_count': portfolio.comments.count(),
            'view_count': portfolio.view_count,
            'like_count': portfolio.like_users.count(),
            'bookmark_count': portfolio.bookmark_users.count()
            })

    return JsonResponse({"tagged_portfolios": tagged_portfolios})


# mypage / 게시글 / 컨택트
@csrf_exempt
def mypage_post_contact(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    contacts_query = mypage_owner.contacts.all()
    contacts = []
    for contact in contacts_query:
        contacts.append({
            'id': contact.id,
            'title': contact.title,
            'thumbnail_url': contact.thumbnail.image.url,
            'comment_count': contact.comments.count(),
            'bookmark_count': contact.bookmark_users.count()
        })

    return JsonResponse({"contacts": contacts})


# mypage / 게시글 / 플레이스
@csrf_exempt
def mypage_post_place(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    places_query = mypage_owner.places.all()
    places = []
    for place in places_query:
        places.append({
            'id': place.id,
            'title': place.title,
            'thumbnail_url': place.thumbnail.image.url,
            'comment_count': place.comments.count(),
            'like_count': place.like_users.count(),
            'bookmark_count': place.bookmark_users.count()
        })

    return JsonResponse({"places": places})



# mypage / 저장 목록 / 포트폴리오
@csrf_exempt
def mypage_bookmark_portfolio(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    bookmarked_portfolios_query = Portfolio.objects.filter(bookmark_users=mypage_owner)
    bookmarked_portfolios = []
    for portfolio in bookmarked_portfolios_query:
        bookmarked_portfolios.append({
            'id': portfolio.id,
            'title': portfolio.title,
            'thumbnail_url': portfolio.thumbnail.image.url,
            'comment_count': portfolio.comments.count(),
            'view_count': portfolio.view_count,
            'like_count': portfolio.like_users.count(),
            'bookmark_count': portfolio.bookmark_users.count(),
        })
    
    return JsonResponse({"bookmarked_portfolios": bookmarked_portfolios})


# mypage / 저장 목록 / 컨택트
@csrf_exempt
def mypage_bookmark_contact(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    bookmarked_contacts_query = Contact.objects.filter(bookmark_users=mypage_owner)
    bookmarked_contacts = []
    for contact in bookmarked_contacts_query:
        bookmarked_contacts.append({
            'id': contact.id,
            'title': contact.title,
            'thumbnail_url': contact.thumbnail.image.url,
            'comment_count': contact.comments.count(),
            'bookmark_count': contact.bookmark_users.count(),
        })
    
    return JsonResponse({"bookmarked_contacts": bookmarked_contacts})


# mypage / 저장 목록 / 플레이스
@csrf_exempt
def mypage_bookmark_place(request):
    data = json.loads(request.body)
    mypage_owner_id = data["user_id"]
    mypage_owner = get_object_or_404(User, user_identifier=mypage_owner_id)
    bookmarked_places_query = Place.objects.filter(bookmark_users=mypage_owner)
    bookmarked_places = []
    for place in bookmarked_places_query:
        bookmarked_places.append({
            'id': place.id,
            'title': place.title,
            'thumbnail_url': place.thumbnail.image.url,
            'comment_count': place.comments.count(),
            'like_count': place.like_users.count(),
            'bookmark_count': place.bookmark_users.count(),
        })
    
    return JsonResponse({"bookmarked_places": bookmarked_places})


# ----profile 관련----
@required_login
@allowed_user
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
            return render(request, 'profile/profile_update.html', ctx)
    elif request.method == 'GET':
        form = ProfileModifyForm(instance=request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/profile_update.html', ctx)

# TODO : 기존과 같은 비밀번호로 바꿔도 바뀜...
@required_login
@local_user
def password_change(request):
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
            return render(request, 'profile/password_change.html', ctx)
    elif request.method == 'GET':
        form = LocalPasswordChangeForm(request.user)
        ctx = {
            'form': form,
        }
        return render(request, 'profile/password_change.html', ctx)


# ----recovery password 관련----
def recovery_pw(request):
    if request.method == 'GET':
        form = RecoveryPwForm()
        ctx = {
            'form': form,
        }
        return render(request, 'profile/recovery_pw.html', context=ctx)


# ajax 방식
@csrf_exempt
def recovery_pw_send_email(request):
    try:
        req = json.loads(request.body)
        user_id = req['user_id']
        username = req['username']
        email = req['email']
        user = User.objects.get(user_id=user_id, username=username, email=email)

        if user is not None:
            if user.is_social or not user.is_ToS:
                return JsonResponse(data={'status': 'false','message': '해당 계정은 소셜 계정입니다.'}, status=500)
            elif not user.is_active:
                return JsonResponse(data={'status': 'false','message': '해당 계정은 회원가입 후 이메일 인증이 완료되지 않았습니다. 먼저 인증을 완료해주세요.'}, status=500)
            else:
                auth_num = email_auth_num()
                user.auth = auth_num
                user.save()

                send_mail(
                    "[masterpic's]: {}님의 비밀번호 찾기 인증메일 입니다.".format(user.user_id),
                    [email],
                    html=render_to_string('profile/recovery_pw_email.html', {
                        'auth_num': auth_num,
                    }),
                )
    except User.DoesNotExist:
        return JsonResponse(data={'status': 'false','message': '입력하신 정보가 일치하지 않거나 존재하지 않습니다.'}, status=500)
        
    return JsonResponse({"user_id": user.user_id})


# ajax 방식
@csrf_exempt
def recovery_pw_auth(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    input_auth_num = req['input_auth_num']
    user = User.objects.get(user_id=user_id, auth=input_auth_num)
    user.auth = ""
    user.save()
    request.session['auth'] = user.user_id
    return JsonResponse({"user_id": user.user_id})


def recovery_pw_reset(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied
        else:
            reset_pw_form = CustomSetPasswordForm(request.user)
            return render(request, 'profile/recovery_pw_reset.html', {'form': reset_pw_form})

    elif request.method == 'POST':
        session_user = request.session['auth']
        user = User.objects.get(user_id=session_user)
        auth_login(request, user,
                   backend='django.contrib.auth.backends.ModelBackend')

        reset_pw_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_pw_form.is_valid():
            user = reset_pw_form.save()
            # messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인하세요.")
            auth_logout(request)
            return redirect('profile:login')
        else:
            auth_logout(request)
            request.session['auth'] = session_user
            return render(request, 'profile/recovery_pw_reset.html', {'form': reset_pw_form})




# ----약관 및 부가설명 관련----
def terms_of_service_use(request):
    return render(request, 'profile/terms_of_service_use.html')