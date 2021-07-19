from django.shortcuts import render

# Create your views here.


def main_list(request):

    # TODO: portfolio, contact, place context 전송하기
    # TODO: 컨택은 최신순, 플레이스는 좋아요순, 메거진은 랜덤

    ctx = {}
    return render(request, 'core/main_list.html', context=ctx)
