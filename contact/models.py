from django.db import models
from django.db.models.enums import Choices
from core.utils import uuid_name_upload_to, compress
from user.models import User
from core.models import *
import json
from django.shortcuts import get_object_or_404


PAY_CUSTOM = 0
PAY_NEGO = 1
PAY_FREE = 2

class PayType(models.IntegerChoices):
    PAY_CUSTOM = 0, '페이 입력'
    PAY_NEGO = 1, '상호 무페이'
    PAY_FREE = 2, '페이 협의'


class Contact(PostBase):

    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)

    file_attach = models.FileField(null=True)
    location = models.ForeignKey(
        to=Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField(blank=True, default=0)
    pay_type = models.IntegerField(choices=PayType.choices, default=PayType.PAY_CUSTOM)

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
