from django.db import models

from user.models import User
from core.models import Tag
from core.models import Location

import json

from .utils import uuid_name_upload_to


class Contact(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='contact_save_users', blank=True)
    desc = models.TextField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='contacts', blank=True)

    # specific field
    file_attach = models.FileField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def to_json(self):
        return {
            "pk": self.pk,
            "title": self.title,
            "pay": self.pay,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "address": self.location.address,
            "lat": self.location.lat,
            "lon": self.location.lon,
        }

    def classname(self):
        return self.__class__.__name__
