from django.shortcuts import get_object_or_404, render
from portfolio.models import Portfolio
from contact.models import Contact
from place.models import Place
from .models import Image
# for Category, Sort
from django.db.models import Q, Count

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

def delete_image(pk):
    image = get_object_or_404(Image,pk=pk)
    image.delete()