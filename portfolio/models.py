from django.db import models

from user.models import User
from core.models import Tag

# for view_count
from django.utils import timezone

from .utils import uuid_name_upload_to


# TODO 전체참여자를 participant로 넣고 중계 모델 만들기
# TODO class Participants portfolio 1개 participant 1명
# TODO 지민이의 의견 -> 시영이에게 물어봐야 함 -> 지민아 화이팅
# TODO 수빈쓰 아이디어 ㄱ

class Portfolio(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="portfolios", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='portfolios', blank=True)

    # TODO Like count 추가, like_users의 내용 확인 (필요 여부 확인)

    def classname(self):
        return self.__class__.__name__


# TODO: 다중이미지 core로 이동 @ 호영
class Images(models.Model):
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True, null=True, verbose_name='Image')
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# # TODO: ViewCount core로 이동(삭제)
# class ViewCount(models.Model):
#     ip = models.CharField(max_length=15, default=None, null=True)
#     post = models.ForeignKey(Portfolio, default=None, null=True,
#                              related_name='view_counts', on_delete=models.CASCADE)
#     date = models.DateField(default=timezone.now, null=True, blank=True)


# TODO Portfolio Comment depth 한개
    # comment, portfolio, self 대댓글


class PortfolioComment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class PortfolioInformation(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
