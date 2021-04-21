from django.db import models
from .utils import uuid_name_upload_to
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from user.models import User
import re


class Location(models.Model):

    # location
    address = models.TextField()  # 도로명 주소
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)

    def __str__(self):
        return self.address


class Tag(models.Model):

    tag = models.CharField(max_length=30)
    save_users = models.ManyToManyField(
        to=User, related_name="tag_save_users", blank=True
    )
    like_users = models.ManyToManyField(
        to=User, related_name="tag_like_users", blank=True
    )

    @classmethod
    def add_tags(selt, tag_str):
        # NOTE: self.desc 말고 TAG FIELD 따로 만들까?
        tags = re.findall(r"#(\w+)\b", tag_str)
        tag_lst = []

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(tag=t)
            tag_lst.append(tag)

        return tag_lst

    def __str__(self):
        return self.tag


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
