from .models import Location, Tag
from rest_framework import serializers


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, validated_data):
        tag, _ = Tag.objects.get_or_create(validated_data)

        return tag