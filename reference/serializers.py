from rest_framework import serializers
from .models import Reference
from core.serializers import TagSerializer


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Reference
        fields = "__all__"
