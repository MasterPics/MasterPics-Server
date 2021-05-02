from rest_framework import serializers
from .models import Reference


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reference
        fields = "__all__"
