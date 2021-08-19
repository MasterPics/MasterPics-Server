from django.shortcuts import get_object_or_404, render
from portfolio.models import Portfolio
from contact.models import Contact
from place.models import Place
from .models import Image
# for Category, Sort
from django.db.models import Q, Count
from django.http import HttpResponse #image delete ajax test

# Create your views here.


def main_list(request):

    # portfolio는 랜덤으로 5개, contact은 최신순으로 4개, place는 좋아요순으로 3개
    portfolios = Portfolio.objects.all().order_by('?')[:5]
    contacts = Contact.objects.all().order_by('-created_at')[:4]
    places = Place.objects.all().annotate(num_save=Count('like_users')).order_by('-num_save')[:3]

    ctx = {
        'portfolios': portfolios,
        'contacts': contacts,
        'places': places,
    }
    return render(request, 'core/main_list.html', context=ctx)

#이미지 삭제 위해 호출되는 함수 #image delete ajax test
def delete_image(request,pk):
    image = get_object_or_404(Image,pk=pk)
    print("삭제될 이미지",image)
    #image.delete()
    return HttpResponse("success")