from rest_framework import serializers
from contact.models import Contact, Comment
from django.contrib.auth import authenticate


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
