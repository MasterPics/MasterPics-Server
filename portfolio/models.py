from django.db import models
from user.models import User
from core.models import Comment, Information

# for view_count
from django.utils import timezone
from .utils import uuid_name_upload_to, compress

from taggit.managers import TaggableManager
from taggit.models import (
    TagBase, TaggedItemBase
)

# TODO 전체참여자를 participant로 넣고 중계 모델 만들기
# TODO class Participants portfolio 1개 participant 1명

class Tag(TagBase):

    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )


class TaggedPortfolio(TaggedItemBase):
    content_object = models.ForeignKey('Portfolio', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'Tag', related_name='tagged_portfolios', on_delete=models.CASCADE, null=True)


class Portfolio(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="portfolios", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()
    tags = TaggableManager(
        verbose_name='tags', help_text='A comma-separated list of tags.', blank=True, through=TaggedPortfolio)

    def save(self, *args, **kwargs):
        compressed_img = compress(self.thumbnail)
        self.thumbnail = compressed_img
        super().save(*args, **kwargs)

    def classname(self):
        return self.__class__.__name__

class PortfolioParticipant(models.Model):
    portfolio = models.ForeignKey(
        to=Portfolio, related_name='participants', on_delete=models.CASCADE)
    participant = models.ForeignKey(
        to=User, related_name='participants', on_delete=models.CASCADE)

# FIXME: 다중이미지 core로 이동 @ 호영
class Images(models.Model):
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True, null=True, verbose_name='Image')
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        compressed_img = compress(self.image)
        self.image = compressed_img
        super().save(*args, **kwargs)

class PortfolioComment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True)

class PortfolioInformation(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, related_name='portfolioInformation_set', on_delete=models.CASCADE)

# class PortfolioParticipant(models.Model):
#     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
#     participant = models.ForeignKey(User, on_delete=models.CASCADE)
