from rest_framework import serializers
from core.models import Tag
from core.serializers import TagSerializer, LocationSerializer
from user.serializers import UserSerializer
from .models import Place


class PlaceSerializers(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    location = LocationSerializer()
    thumbnail = serializers.ImageField(required=False)

    class Meta:
        model = Place
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        tags_list = []
        for tag_data in tags_data:
            new_tag = Tag.objects.get_or_create(**tag_data)[0]
            print(new_tag)
            tags_list.append(new_tag)

        location_data = validated_data.pop("location")
        location_serializer = LocationSerializer(data=location_data)
        location_serializer.is_valid(raise_exception=True)
        location = location_serializer.save()

        place = Place.objects.create(**validated_data, location=location)
        place.tags.set(tags_list)
        return place