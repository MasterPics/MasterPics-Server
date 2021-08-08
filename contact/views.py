from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from core.models import *

# for Comment, Save
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# for Comment, Save, Map
import json

# for location
from core.forms import LocationForm

# for Sort, Category, Search
from django.db.models import Count, Q

# for infinite scroll
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@csrf_exempt
def contact_save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_id = data["contact_id"]
        contact = get_object_or_404(Contact, pk=contact_id)
        is_saved = request.user in contact.bookmark_users.all()
        if is_saved:
            contact.bookmark_users.remove(
                get_object_or_404(User, pk=request.user.pk))
        else:
            contact.bookmark_users.add(
                get_object_or_404(User, pk=request.user.pk))
        is_saved = not is_saved
        contact.save()
        return JsonResponse({'contact_id': contact_id, 'is_saved': is_saved})


def contact_list(request):
    contacts = Contact.objects.all()

    # 상호무페이
    no_pay = request.GET.get('no_pay', False)
    if no_pay == 'true':
        contacts = Contact.objects.all().filter(pay=0).distinct()
    else:
        contacts = Contact.objects.all()

    category = request.GET.get('category', 'all')  # Category
    sort = request.GET.get('sort', 'recent')  # Sort
    search = request.GET.get('search', '')  # Search

    # Category
    if category != 'all':
        if category == User.CATEGORY_PHOTOGRAPHER:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_PHOTOGRAPHER)
                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_MODEL:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_MODEL)
                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_HM:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_HM)
                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_STYLIST:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_STYLIST)
                                       ).distinct().order_by("?")
        elif category == User.CATEGORY_OTHERS:
            contacts = contacts.filter(Q(user__category=User.CATEGORY_OTHERS)
                                       ).distinct().order_by("?")

    # Sort
    if sort == 'save':
        contacts = contacts.annotate(num_save=Count(
            'contactinformation')).order_by('-num_save', '-created_at')
    elif sort == 'pay':
        contacts = contacts.order_by('-pay', '-created_at')
    elif sort == 'recent':
        contacts = contacts.order_by('-created_at')

    # Search
    if search:
        contacts = contacts.filter(
            Q(title__icontains=search) |  # 제목검색
            Q(desc__icontains=search) |  # 내용검색
            Q(user__username__icontains=search)  # 질문 글쓴이검색
        ).distinct()

    # infinite scroll
    contacts_per_page = 6
    page = request.GET.get('page', 1)
    paginator = Paginator(contacts, contacts_per_page)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'contacts': contacts,
        'sort': sort,
        'category': category,
        'search': search,
    }
    return render(request, 'contact/contact_list.html', context=context)


def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    comments = contact.comments.all()
    ctx = {
        'contact': contact,
        'comments': comments
    }
    return render(request, 'contact/contact_detail.html', context=ctx)


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "삭제되었습니다.")
        return redirect('contact:contact_list')
    else:
        ctx = {'contact': contact}
        return render(request, 'contact/contact_delete.html', context=ctx)


@login_required
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        location_form = LocationForm(request.POST, instance=contact.location)

        if form.is_valid() and location_form.is_valid():
            contact = form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            contact.user = request.user
            contact.location = location
            contact.save()

            for i, image in enumerate(request.FILES.getlist('images')):

                image_obj = PostImage()
                image_obj.post = Contact.objects.get(id=contact.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

                # if not i:
                #     contact.thumbnail = image_obj.image
                #     contact.save()

            return redirect('contact:contact_detail', contact.pk)
    else:
        form = ContactForm(instance=contact)
        images = contact.post_image_images.all()
        location_form = LocationForm(instance=contact)
        ctx = {'form': form,
               'location_form': location_form,
               'images': images}
        return render(request, 'contact/contact_update.html', ctx)

# TODO 파일 첨부


@login_required
def contact_create(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        if contact_form.is_valid() and location_form.is_valid():
            contact = contact_form.save(commit=False)
            location = location_form.save(commit=False)
            location.save()
            contact.user = request.user
            contact.location = location
            contact.save()

            for i, image in enumerate(request.FILES.getlist('images')):

                image_obj = PostImage()
                image_obj.post = Contact.objects.get(id=contact.id)
                img = Image.objects.create(image=image)
                #img.save()
                image_obj.image = img
                image_obj.save()

                if not i:
                    contact.thumbnail = image_obj.image
                    contact.save()
            return redirect('contact:contact_detail', contact.pk)
        
        #TODO Else 문 로직 정리해줘야함 
        else:
            return redirect("contact:contact_list")


    else:
        ctx = {
            'contact_form': ContactForm(),
            'location_form': LocationForm(),
        }
        return render(request, 'contact/contact_create.html', ctx)


def contact_map(request):
    contacts = Contact.objects.filter(is_closed=False)
    ctx = {
        'contacts_json': json.dumps([contact.to_json() for contact in contacts])
    }
    return render(request, 'contact/contact_map.html', context=ctx)


############################### comment ###############################
@csrf_exempt
def contact_comment_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contact_id = data['id']
        comment_value = data['value']
        contact = Contact.objects.get(id=contact_id)
        comment = Comment.objects.create(
            writer=request.user, post=contact, content=comment_value)
        return JsonResponse({'contact_id': contact_id, 'comment_id': comment.id, 'value': comment_value})


@csrf_exempt
def contact_comment_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data['commentId']
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'comment_id': comment_id})
