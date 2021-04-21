from django.shortcuts import render


def main_list(request):
    ctx = {}
    return render(request, "core/main_list.html", context=ctx)


from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer


class LocationViewsets(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer