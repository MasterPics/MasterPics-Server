from rest_framework import serializers
from contact.models import Contact, Comment
from django.contrib.auth import authenticate
from core.serializers import LocationSerializer

from user.serializers import UserSerializer


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"
