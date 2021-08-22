from django.shortcuts import redirect
from functools import wraps

# 약관 동의한 유저(로컬 유저 + 소셜 회원가입 후 추가 정보 입력한 유저)만이 접근할 수 있도록 하는 데코레이터
# 약관에 동의하지 않았을 경우 '추가 정보 입력' 페이지로 이동시킴
def allowed_user(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_ToS == True:
            return function(request, *args, **kwargs)
        else:
            return redirect("profile:social_user_more_info")

    return wrap


# 로그인 안 한 유저가 로그인한 유저만 할 수 있는 행위를 할때 로그인 페이지로 이동시키게 하기
def required_login(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = getattr(request, "user")

        if user and user.is_authenticated:
            return function(request, *args, **kwargs)

        path = request.get_full_path()

        return redirect("/profile/login/?next="+ path)
    return wrap


# 로컬 유저만 접근할 수 있도록 하는 데코레이터
# 소셜 유저일 경우 mypage로 이동시키게 하기 (현재 password change만이 소셜 유저가 접근 불가능한 기능이기 때문)
def local_user(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_social == False and request.user.is_ToS == True:
            return function(request, *args, **kwargs)
        else:
            return redirect("profile:mypage")

    return wrap