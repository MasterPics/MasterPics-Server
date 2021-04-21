from rest_framework import serializers
from contact.models import Contact, Comment
from django.contrib.auth import authenticate
from core.models import Location


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    location_address = serializers.CharField()
    location_lat = serializers.FloatField()
    location_lon = serializers.FloatField()

    class Meta:
        model = Contact
        fields = "__all__"
