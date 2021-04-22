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

    def run_validators(self, value):
        return super().run_validators(value)

    def create(self, validated_data):
        return super().create(validated_data)