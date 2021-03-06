from django.db import models
from django.db.models.fields.related import ForeignKey
from .utils import uuid_name_upload_to, compress
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from user.models import User
import re

import os
from uuid import uuid4
from django.utils import timezone

from taggit.models import TagBase, TaggedItemBase
from taggit.managers import TaggableManager

from django.db.models.signals import post_delete
from django.dispatch import receiver

""" commnet 시간 """
from datetime import datetime, timedelta


class Location(models.Model):
    address = models.TextField()  # 도로명 주소
    lat = models.FloatField(blank=True, null=True)  # 위도
    lon = models.FloatField(blank=True, null=True)  # 경도

    def __str__(self):
        return self.address

    def to_json(self):
        return {"address": self.address,
                "lat": self.lat,
                "lon": self.lon
                }


class Tag(TagBase):

    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )


# TODO: 다중 이미지 최대 제한
class Image(models.Model):
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        compressed_img = compress(self.image)
        self.image = compressed_img
        super().save(*args, **kwargs)


class PostBase(models.Model):

    # meta info
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()
    view_count = models.IntegerField(default=0)

    # MTM fields
    like_users = models.ManyToManyField(
        User, related_name='likes', through='PostLike')
    bookmark_users = models.ManyToManyField(
        User, related_name='bookmarks', through='PostBookmark')
    tags = TaggableManager(
        verbose_name='tags', help_text='해시태그를 입력해주세요', blank=True, through='TaggedPost')
    images = models.ManyToManyField(
        Image, related_name='images', through='PostImage')

    # foreing key
    thumbnail = models.ForeignKey('Image', related_name="thumbnail",
                                  on_delete=models.SET_NULL, blank=True, null=True, default=None) #SET_NULL은 update시 thumbnail 바뀔경우 위해

    def classname(self):
        return self.__class__.__name__


class PostImage(models.Model):
    post = models.ForeignKey(
        to=PostBase, related_name='post_image_images', on_delete=models.CASCADE)
    image = models.ForeignKey(to=Image, on_delete=models.CASCADE)

@receiver(post_delete, sender=PostImage)
def file_delete_action(sender, instance, **kwargs):
    instance.image.delete(False)


class PostLike(models.Model):
    user = models.ForeignKey(
        User, related_name='user_post_like', on_delete=models.CASCADE)
    post = models.ForeignKey(
        PostBase, related_name='post_post_like', on_delete=models.CASCADE)


class PostBookmark(models.Model):
    user = models.ForeignKey(
        to=User, related_name='user_post_bookmark', on_delete=models.CASCADE)
    post = models.ForeignKey(
        to=PostBase, related_name='post_post_bookmark', on_delete=models.CASCADE)


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey(PostBase, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        to=Tag, related_name='tag_tagged_post', on_delete=models.CASCADE, null=True)


class Comment(models.Model):

    writer = models.ForeignKey(
        User, related_name="writer_set", on_delete=models.PROTECT)
    post = models.ForeignKey(
        to=PostBase, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey(
        to='self', related_name='child_comments', on_delete=models.PROTECT, null=True)
    deleted = models.BooleanField(default=False)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False

    class Meta:
        ordering = ['-created_at']
