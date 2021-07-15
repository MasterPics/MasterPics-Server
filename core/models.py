from django.db import models
from .utils import uuid_name_upload_to, compress
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from user.models import User
import re

import os
from uuid import uuid4
from django.utils import timezone

from taggit.models import TagBase



class Location(models.Model):
    address = models.TextField()  # 도로명 주소
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)

    def __str__(self):
        return self.address


class Comment(models.Model):
    writer = models.ForeignKey(
        User, related_name="writer_set", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Information(models.Model):
    save_users = models.ManyToManyField(
        to=User, related_name='save_users', blank=True)
    like_users = models.ManyToManyField(
        to=User, related_name='like_users', blank=True)
    like_counter = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)


class Images(models.Model):
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        compressed_img = compress(self.image)
        self.image = compressed_img
        super().save(*args, **kwargs)


class Tag(TagBase):

    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )

