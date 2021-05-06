from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

from core.models import Tag


# for Save, Like
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# for Category, Sort
from django.db.models import Q, Count

# for infinite scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for multiple images
from django.forms import modelformset_factory


# TODO @api_view(['GET'])
def portfolio_list(request):
    portfolios = Portfolio.objects.all().order_by("?")
    request_user = request.user  # 로그인한 유저

    category = request.GET.get('category', 'all')  # Category
    sort = request.GET.get('sort', 'recent')  # Sort
    search = request.GET.get('search', '')  # Search

    # Category, order_by("?"): random 으로 선택
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_MODEL)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_HM)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_STYLIST)
                                           ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_OTHERS)
                                           ).distinct().order_by("?")

    # Sort 최신순, 조회순, 좋아요순, 저장순

    if sort == 'recent':
        portfolios = portfolios.order_by('-updated_at')
    elif sort == 'view':
        portfolios = portfolios.order_by('-view_count', '-updated_at')
    elif sort == 'like':
        portfolios = portfolios.annotate(num_save=Count(
            'like_users')).order_by('-num_save', '-updated_at')
    elif sort == 'save':
        portfolios = portfolios.annotate(num_save=Count(
            'save_users')).order_by('-num_save', '-updated_at')

    # Search
    if search:
        portfolios = portfolios.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # infinite scroll
    portfolios_per_page = 6
    page = request.GET.get('page', 1)
    paginator = Paginator(portfolios, portfolios_per_page)
    try:
        portfolios = paginator.page(page)
    except PageNotAnInteger:
        portfolios = paginator.page(1)
    except EmptyPage:
        portfolios = paginator.page(paginator.num_pages)

    context = {'portfolios': portfolios, 'request_user': request.user, 'sort': sort,
               'category': category, }
    return render(request, 'portfolio/portfolio_list.html', context=context)


def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    images = portfolio.portfolio_images.all()
    num_of_imgs = images.count

    tags = portfolio.tags.all()

    portfolio_owner = portfolio.user  # 게시글 작성자
    request_user = request.user  # 로그인한 유저

    # 조회수(view_count)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)

    try:
        view_counts = ViewCount.objects.get(ip=ip, post=portfolio)
    except Exception as e:
        print(e)
        view_counts = ViewCount(ip=ip, post=portfolio)
        Portfolio.objects.filter(pk=pk).update(
            view_count=portfolio.view_count+1)
        view_counts.save()
    else:
        if not view_counts.date == timezone.localtime().date():
            Portfolio.objects.filter(pk=pk).update(
                view_count=portfolio.view_count+1)
            view_counts.date = timezone.localtime()
            view_counts.save()
        else:
            print(str()+'has already hit his post.\n\n')

    ctx = {'portfolio': portfolio,
           'images': images,
           'tags': tags,
           'portfolio_owner': portfolio_owner,
           'request_user': request_user,
           'num_of_imgs': num_of_imgs, }
    return render(request, 'portfolio/portfolio_detail.html', context=ctx)


@login_required
def portfolio_delete(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    owner = portfolio.user  # 게시글 작성자
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, "삭제되었습니다.")

        return redirect('profile:profile_detail_posts', owner.id)
    else:
        ctx = {'portfolio': portfolio}
        return render(request, 'portfolio/portfolio_delete.html', context=ctx)


@login_required
def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            portfolio.image = request.FILES.get('image')

            portfolio.tags.all().delete()

            # save tag
            tags = Tag.add_tags(portfolio.tag_str)
            for tag in tags:
                portfolio.tags.add(tag)

            return redirect('portfolio:portfolio_detail', portfolio.id)
    else:
        form = PortfolioForm(instance=portfolio)
        ctx = {'form': form, }
        return render(request, 'portfolio/portfolio_update.html', ctx)


@login_required
def portfolio_create(request):
    # 'extra' : number of photos
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,)

        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            portfolio.image = request.FILES.get('images')
            for image in request.FILES.getlist('images'):
                image_obj = Images()
                image_obj.portfolio_id = portfolio.id
                image_obj.image = image
                image_obj.save()

            messages.success(request, "posted!")

            # TODO tag 처리
            # # prev_tag
            # prev_tags = Tag.objects.all()
            # save tag
            tags_portfolio = Tag.add_tags(portfolio.tag_str)
            for tag in tags_portfolio:
                portfolio.tags.add(tag)

            # # tag compare
            # # tags_portfolio의 tag가 tag_all에 있는지 확인하고
            # # 이미 있으면 do nothing
            # # 없으면 tag 게시물 create
            # local_create(request, prev_tags)

            return redirect('portfolio:portfolio_detail', portfolio.pk)
        else:
            print(form.errors, formset.errors)

    else:
        form = PortfolioForm()
        ctx = {'form': form}

    return render(request, 'portfolio/portfolio_create.html', ctx)


@csrf_exempt
def portfolio_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        portfolio_id = data["portfolio_id"]
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        request_user = request.user
        is_saved = request_user in portfolio.save_users.all()
        if is_saved:
            portfolio.save_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            portfolio.save_users.add(
                get_object_or_404(User, pk=request_user.pk))
        is_saved = not is_saved
        portfolio.save()
        return JsonResponse({'portfolio_id': portfolio_id, 'is_saved': is_saved})


@csrf_exempt
def portfolio_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        portfolio_id = data["portfolio_id"]
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        request_user = request.user
        is_liked = request_user in portfolio.like_users.all()
        if is_liked:
            portfolio.like_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            portfolio.like_users.add(
                get_object_or_404(User, pk=request_user.pk))
        is_liked = not is_liked
        portfolio.save()
        return JsonResponse({'portfolio_id': portfolio_id, 'is_liked': is_liked})
