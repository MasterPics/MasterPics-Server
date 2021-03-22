from django.db import models
from django_mysql.models import ListCharField

# TODO import 위치
from user.models import User
from core.models import Tag

from .utils import uuid_name_upload_to


class Reference(models.Model):
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    save_users = models.ManyToManyField(
        to=User, related_name='reference_save_users', blank=True)
    like_users = models.ManyToManyField(
        to=User, related_name='reference_like_users', blank=True)
    desc = models.TextField()
    image_url = ListCharField(base_field=models.CharField(
        max_length=100), max_length=60000)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='references', blank=True)
