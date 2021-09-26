from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from core.forms import PostImageForm
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

# for required_login
from user.decorators import required_login


def portfolio_list(request):

    portfolios = Portfolio.objects.all().order_by("-created_at")

    category = request.GET.get('category', 'all')  # Category
    sort = request.GET.get('sort', 'recent')  # Sort
    search = request.GET.get('search', '')  # Search

    # Category, order_by("created_at"): random 으로 선택
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                           ).distinct().order_by('-created_at')
        elif category == User.CATEGORY_MODEL:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_MODEL)
                                           ).distinct().order_by('-created_at')
        elif category == User.CATEGORY_HM:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_HM)
                                           ).distinct().order_by('-created_at')
        elif category == User.CATEGORY_STYLIST:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_STYLIST)
                                           ).distinct().order_by('-created_at')
        elif category == User.CATEGORY_OTHERS:
            portfolios = portfolios.filter(Q(user__category=User.CATEGORY_OTHERS)
                                           ).distinct().order_by('-created_at')

    # Sort 최신순, 조회순, 좋아요순, 저장순
    if sort == 'recent':
        portfolios = portfolios.order_by('-created_at')
    elif sort == 'view':
        portfolios = portfolios.order_by('-view_count', '-created_at')
    elif sort == 'like':
        portfolios = portfolios.annotate(num_save=Count(
            'like_users')).order_by('-num_save', '-created_at')
    elif sort == 'save':
        portfolios = portfolios.annotate(num_save=Count(
            'bookmark_users')).order_by('-num_save', '-created_at')

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

    context = {'portfolios': portfolios,
               'sort': sort,
               'category': category, }

    return render(request, 'portfolio/portfolio_list.html', context=context)


def portfolio_detail(request, pk):

    portfolio = Portfolio.objects.get(pk=pk)
    portfolio.view_count += 1
    portfolio.save()

    parent_comments = portfolio.comments.all().filter(parent_comment__isnull=True)

    ctx = {
        'portfolio': portfolio,
        'images': portfolio.images.all(),
        'tags': portfolio.tags.all(),
        'comments': parent_comments,
        'like_users': portfolio.like_users.all(),
        'bookmark_users': portfolio.bookmark_users.all()
    }

    return render(request, 'portfolio/portfolio_detail.html', context=ctx)


@required_login
def portfolio_delete(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    owner = portfolio.user  # 게시글 작성자
    if request.method == 'POST':
        portfolio.delete()
        for image in portfolio.post_image_images.all():
            image.delete()

        messages.success(request, "삭제되었습니다.")

        return redirect('portfolio:portfolio_list')
    else:
        ctx = {'portfolio': portfolio}
        return render(request, 'portfolio/portfolio_delete.html', context=ctx)


@required_login
def portfolio_update(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            # portfolio.save()
            portfolio.tags.clear()
            form.save_m2m()

            if not PostImage.objects.filter(post=portfolio) and not request.FILES.getlist('images'):
                ctx = {
                    'form': form,
                    'images': portfolio.post_image_images.all(),
                    'image_error': '사진은 1장 이상이어야 합니다.'
                }
                return render(request, 'portfolio/portfolio_update.html', ctx)
            
            for i, image in enumerate(request.FILES.getlist('images')):
                image_obj = PostImage()
                image_obj.post = Portfolio.objects.get(id=portfolio.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

            images=portfolio.post_image_images.all()
            if images:
                portfolio.thumbnail = images[0].image
                portfolio.save()
            else: #사진이 아무것도 안남았을때
                portfolio.thumbnail = None

            return redirect('portfolio:portfolio_detail', portfolio.id)

        #TODO Post 인데 Form not Valid일때 어떻게 처리할지 
    else:
        form = PortfolioForm(instance=portfolio)
        images = portfolio.post_image_images.all()
        ctx = {
            'form': form,
            'images': images
        }
        return render(request, 'portfolio/portfolio_update.html', ctx)


@required_login
def portfolio_create(request):
    # 'extra' : number of photos
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)

        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            # portfolio.save()
            # form.save_m2m()

            if not request.FILES.getlist('images'):
                ctx = {
                    'form': form,
                    'image_error': '사진은 1장 이상이어야 합니다.',
                }
                return render(request, 'portfolio/portfolio_create.html', ctx)
            else:
                portfolio.save()
                form.save_m2m()

            for i, image in enumerate(request.FILES.getlist('images')):
                image_obj = PostImage()
                image_obj.post = Portfolio.objects.get(id=portfolio.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

                if not i:
                    portfolio.thumbnail = image_obj.image
                    portfolio.save()
            # messages.success(request, "posted!")
            return redirect('portfolio:portfolio_detail', portfolio.pk)
        
        else:
            ctx = {
                'form': form
            }
            return render(request, 'portfolio/portfolio_create.html', ctx)

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
        is_saved = request_user in portfolio.bookmark_users.all()
        if is_saved:
            portfolio.bookmark_users.remove(
                get_object_or_404(User, pk=request_user.pk))
        else:
            portfolio.bookmark_users.add(
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


############################### comment ###############################
@csrf_exempt
def portfolio_comment_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            login_required = False 
            data = json.loads(request.body)
            portfolio_id = data['id']
            comment_value = data['value']
            portfolio = Portfolio.objects.get(id=portfolio_id)
            comment = Comment.objects.create(
                writer=request.user, post=portfolio, content=comment_value)
            return JsonResponse({'portfolio_id': portfolio_id, 'comment_id': comment.id, 'value': comment_value, 'login_required':login_required})
        else:
            login_required = True
            return JsonResponse({'login_required': login_required})

@csrf_exempt
def portfolio_comment_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data['commentId']
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'comment_id': comment_id})
