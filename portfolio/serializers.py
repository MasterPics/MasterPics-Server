from rest_framework import serializers
from user.serializers import UserSerializer
from core.serializers import TagSerializer
from core.models import Tag
from .models import Portfolio


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Portfolio
        fields = [
            "url",
            "user",
            "thumbnail",
            "title",
            "desc",
            "tags",
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        tags_list = []
        for tag_data in tags_data:
            new_tag = Tag.objects.get_or_create(**tag_data)[0]
            print(new_tag)
            tags_list.append(new_tag)

        portfolio = Portfolio.objects.create(**validated_data)
        portfolio.tags.set(tags_list)
        return portfolio