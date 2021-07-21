from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
import json

# infinite loading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from core app
from core.forms import *

# from place app
from .models import *
from .forms import *

# for Comment, Save
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def place_create(request):

    if request.method == 'POST':
        place_form = PlaceForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)

        if place_form.is_valid() and location_form.is_valid():
            place = place_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            place.user = request.user
            place.location = location
            place.save()
            place_form.save_m2m()

            for i, image in enumerate(request.FILES.getlist('images')):

                image_obj = PostImage()
                image_obj.post = Place.objects.get(id=place.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

                if not i:
                    place.thumbnail = image_obj.image
                    place.save()

            print(place.tags.all())

            return redirect('place:place_detail', place.pk)

    else:
        place_form = PlaceForm()
        location_form = LocationForm()

    ctx = {
        'location_form': location_form,
        'place_form': place_form,
    }

    return render(request, 'place/place_create.html', context=ctx)


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)

    ctx = {
        'place': place,
        'tags': place.tags.all(),
        'images': place.images.all(),
        'comments': place.comments.all(),
    }

    return render(request, 'place/place_detail.html', context=ctx)


# TODO Update에서 썸네일 안 넘어가는 것 수정해야 함
@login_required
def place_update(request, pk):
    place = get_object_or_404(Place, pk=pk)

    if request.method == 'POST':
        place_form = PlaceForm(request.POST, request.FILES, instance=place)
        location_form = LocationForm(request.POST, instance=place.location)
        
        if place_form.is_valid() and location_form.is_valid():
            place_update = place_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            place_update.user = request.user
            place_update.location = location
            place_update.save()
            place_form.save_m2m()

            for i, image in enumerate(request.FILES.getlist('images')):

                image_obj = PostImage()
                image_obj.post = Place.objects.get(id=place_update.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

                if not i:
                    place_update.thumbnail = image_obj.image
                    place_update.save()
                    
            return redirect('place:place_detail', place.pk)
    else:
        place_form = PlaceForm(instance=place)
        print(dir(place_form))
        location_form = LocationForm(instance=place.location)

        ctx = {
            'place_form': place_form,
            'location_form': location_form,
        }

        return render(request, 'place/place_update.html', context=ctx)


def place_list(request):
    places = Place.objects.all()
    sort = request.GET.get('sort', 'recent')
    search = request.GET.get('search', '')
    no_pay = request.GET.get('no_pay')

    # 상호무페이
    # 0718 상호무페이 필터링 추가
    if no_pay == 'true':
        places = Place.objects.all().filter(pay=0).distinct()
    else:
        places = Place.objects.all()

    # SORT
    if sort == 'pay':
        places = places.order_by('pay')
    elif sort == 'like':  # 0718 like순 정렬 추가
        places = places.order_by('-like_users')
    else:
        places = places.order_by('-created_at')

    if search:
        places = places.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search) |  # 질문 글쓴이검색
            Q(location__address__icontains=search)  # 0718 주소검색
        ).distinct()

    # infinite scroll
    places_per_page = 8
    page = request.GET.get('page', 1)
    paginator = Paginator(places, places_per_page)
    try:
        places = paginator.page(page)
    except PageNotAnInteger:
        places = paginator.page(1)
    except EmptyPage:
        places = paginator.page(paginator.num_pages)

    ctx = {
        'places': places,
        'sort': sort,
        'search': search,
        'request_user': request.user
    }

    return render(request, 'place/place_list.html', context=ctx)


@login_required
def place_delete(request, pk):

    place = get_object_or_404(Place, pk=pk)

    if request.method == 'POST':
        place.location.delete()
        place.delete()
        messages.success(request, '삭제되었습니다.')
        return redirect('place:place_list')

    else:
        ctx = {'place': place}
        return render(request, 'place/place_delete.html', context=ctx)


@csrf_exempt
def place_like(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data["place_id"]
        place = get_object_or_404(Place, pk=place_id)
        is_liked = request.user in place.like_users.all()

        if is_liked:
            place.like_users.remove(
                get_object_or_404(User, pk=request.user.pk)
            )
        else:
            place.like_users.add(
                get_object_or_404(User, pk=request.user.pk)
            )
        is_liked = not is_liked
        place.save()
        return JsonResponse({
            "place_id": place_id,
            "is_liked": is_liked
        })


@csrf_exempt
def place_bookmark(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data["place_id"]
        place = get_object_or_404(Place, pk=place_id)
        is_bookmarked = request.user in place.bookmark_users.all()
        if is_bookmarked:
            place.bookmark_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            place.bookmark_users.add(
                get_object_or_404(User, pk=request.user.pk))
        is_bookmarked = not is_bookmarked
    return JsonResponse({
        'place_id': place_id,
        'is_bookmarked': is_bookmarked
    })


############################### comment ###############################
@csrf_exempt
def place_comment_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data['id']
        comment_value = data['value']
        place = Place.objects.get(id=place_id)
        comment = Comment.objects.create(
            writer=request.user, post=place, content=comment_value)
        return JsonResponse({'place_id': place_id, 'comment_id': comment.id, 'value': comment_value})


@csrf_exempt
def place_comment_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data['commentId']
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'comment_id': comment_id})
