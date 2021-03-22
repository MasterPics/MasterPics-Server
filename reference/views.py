from django.shortcuts import render
from .models import *
from portfolio.models import Portfolio
# TODO tag 위치
from core.models import Tag


def local_list(request):

    tags = Tag.objects.all()

    context = {
        'tags': tags,
        'request_user': request.user,
    }
    return render(request, 'reference/local_list.html', context=context)


def local_detail(request, tag):
    portfolios_taged = Portfolio.objects.filter(tags__tag=tag)

    context = {
        'portfolios_taged': portfolios_taged,
    }
    return render(request, 'reference/local_detail.html', context=context)
