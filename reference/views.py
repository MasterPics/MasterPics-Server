from django.shortcuts import render
from .models import *
from portfolio.models import Portfolio
# TODO tag 위치
from core.models import Tag


def reference_local_list(request):

    tags = Tag.objects.all()

    context = {
        'tags': tags,
    }
    return render(request, 'reference/reference_local_list.html', context=context)


def reference_local_detail(request, tag):
    portfolios_taged = Portfolio.objects.filter(tags__tag=tag)

    context = {
        'portfolios_taged': portfolios_taged,
    }
    return render(request, 'reference/reference_local_detail.html', context=context)
