from django.db import models
from user.models import User
from core.models import Comment, Image
from django.shortcuts import get_object_or_404


# for view_count
from django.utils import timezone
from core.models import *

# for hashtag

# TODO 전체참여자를 participant로 넣고 중계 모델 만들기
# TODO class Participants portfolio 1개 participant 1명


class Portfolio(PostBase):

    user = models.ForeignKey(
        to="user.User", related_name="portfolios", on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        to='user.User', through='Participants')

    def classname(self):
        return self.__class__.__name__


class Participants(models.Model):
    portfolio = models.ForeignKey(
        to='Portfolio', related_name='portfolio_participants', on_delete=models.CASCADE)
    participant = models.ForeignKey(
        to='user.User', related_name='participant_participants', on_delete=models.CASCADE)
