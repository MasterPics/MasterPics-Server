from django.db import models

# TODO import 위치
from user.models import User
from core.models import Tag

# for view_count
from django.utils import timezone

from .utils import uuid_name_upload_to


class Portfolio(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="portfolios", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='portfolio_save_users', blank=True)
    desc = models.TextField()

    # specific field
    view_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(
        to=User, related_name='portfolio_like_users', blank=True)
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='portfolios', blank=True)

    def classname(self):
        return self.__class__.__name__

class Images(models.Model):
    image = models.ImageField(
        upload_to=uuid_name_upload_to, blank=True,null=True, verbose_name='Image')
    portfolio = models.ForeignKey(
        to=Portfolio, null=True, blank=True, related_name='portfolio_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ViewCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)
    post = models.ForeignKey(Portfolio, default=None, null=True,
                             related_name='view_counts', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, null=True, blank=True)
