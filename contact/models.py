from django.db import models
from django.db.models.enums import Choices
from core.utils import uuid_name_upload_to, compress
from user.models import User
from core.models import *
import json
from django.shortcuts import get_object_or_404


class PayType(models.IntegerChoices):
    PAY_FREE = 0, '상호 무페이'
    PAY_NEGO = 1, '페이 협의'
    PAY_CUSTOM = 2, '페이 입력'


class Contact(PostBase):

    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)

    file_attach = models.FileField(null=True)
    location = models.ForeignKey(
        to=Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField(blank=True, default=0)
    pay_type = models.IntegerField(choices=PayType.choices, default=PayType.PAY_FREE)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def to_json(self, request_user):
        return {
            "pk": self.pk,
            "title": self.title,
            "thumbnail" : self.thumbnail.image.url,
            "writer" : self.user.username, 
            "writer_thumbnail" : self.user.image.url,
            "writer_category" : self.user.category,
            "is_saved" : request_user in self.bookmark_users.all(), 
            "pay_type": self.pay_type,
            "pay": self.pay,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "address": self.location.address,
            "lat": self.location.lat,
            "lon": self.location.lon,
        }

    def classname(self):
        return self.__class__.__name__
