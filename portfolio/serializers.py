from rest_framework import serializers
from user.serializers import UserSerializer
from .models import Portfolio


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = "__all__"