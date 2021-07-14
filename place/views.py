from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,Count
import json

# infinite loading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from core app
from core.forms import *

# from place app
from .models import *
from .forms import *

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

            place.image = request.FILES.get('image')
            for i, image in enumerate(request.FILES.getlist('images')):
                image_obj = PlaceImages()
                image_obj.place_id = place.id
                image_obj.image = Images()
                image_obj.image.image = image
                image_obj.image.save()
                image_obj.save()

                if not i:
                    place.thumbnail = image_obj.image
                    place.save()
                else:
                    i += 1

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

    #comment 를 가져오는 쿼리
    comments = PlaceComment.get_comments(place)

    ctx = {
        'place': place,
        'comments': comments,
        'request_user' : request.user
    }

    return render(request, 'place/place_detail.html', context=ctx)


#TODO Update에서 썸네일 안 넘어가는 것 수정해야 함
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
            place_update.location = location
            print(place_form.image)
            place_update.image = request.FILES.get('image')
            place_update.image.save()
            place_update.save()
            return redirect('place:place_detail', place.pk)
    else:
        place_form = PlaceForm(instance=place)
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

    # SORT
    if sort == 'pay':
        places = places.order_by('-pay')
    elif sort == 'save': #save 케이스 정렬 추가
        places = places.order_by('-created_at')
    else:
        places = places.order_by('-created_at')
    

    if search:
        places = places.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
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


def place_map(request):
    places = Place.objects.all()
    ctx = {
        'places_json': json.dumps([places.to_json() for place in places])
    }
    return render(request, 'place/place_map.html', context=ctx)


def place_select(request):
    form = LocationForm()
    ctx = {
        'form': form,
    }
    return render(request, 'place/place_select.html', context=ctx)
