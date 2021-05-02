from django.shortcuts import render
from .models import *

from portfolio.models import Portfolio

from core.models import Tag


# for Save, Like
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# for Category, Sort
from django.db.models import Q, Count

# for infinite scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# django rest framework
from rest_framework import viewsets
from .serializers import ReferenceSerializer


class ReferenceViewSets(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer


def reference_local_list(request):

    tags = Tag.objects.all()

    context = {
        'tags': tags,
    }
    return render(request, 'reference/reference_local_list.html', context=context)


def reference_local_detail(request, tag):
    portfolios_taged = Portfolio.objects.filter(tags__tag=tag)

    request_user = request.user  # 로그인한 유저

    category = request.GET.get('category', 'all')  # Category
    sort = request.GET.get('sort', 'recent')  # Sort
    search = request.GET.get('search', '')  # Search

    # Category, order_by("?"): random 으로 선택
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            portfolios_taged = portfolios_taged.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            portfolios_taged = portfolios_taged.filter(Q(user__category=User.CATEGORY_MODEL)
                                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            portfolios_taged = portfolios_taged.filter(Q(user__category=User.CATEGORY_HM)
                                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            portfolios_taged = portfolios_taged.filter(Q(user__category=User.CATEGORY_STYLIST)
                                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            portfolios_taged = portfolios_taged.filter(Q(user__category=User.CATEGORY_OTHERS)
                                                       ).distinct().order_by("?")

    # Sort 최신순, 조회순, 좋아요순, 저장순

    if sort == 'recent':
        portfolios_taged = portfolios_taged.order_by('-updated_at')
    elif sort == 'view':
        portfolios_taged = portfolios_taged.order_by(
            '-view_count', '-updated_at')
    elif sort == 'like':
        portfolios_taged = portfolios_taged.annotate(num_save=Count(
            'like_users')).order_by('-num_save', '-updated_at')
    elif sort == 'save':
        portfolios_taged = portfolios_taged.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-updated_at')

    # Search
    if search:
        portfolios_taged = portfolios_taged.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # infinite scroll
    portfolios_per_page = 6
    page = request.GET.get('page', 1)
    paginator = Paginator(portfolios_taged, portfolios_per_page)
    try:
        portfolios_taged = paginator.page(page)
    except PageNotAnInteger:
        portfolios_taged = paginator.page(1)
    except EmptyPage:
        portfolios_taged = paginator.page(paginator.num_pages)

    context = {
        'portfolios_taged': portfolios_taged,
        'request_user': request.user,
        'sort': sort,
        'category': category,
        'tag': tag,
    }
    return render(request, 'reference/reference_local_detail.html', context=context)
