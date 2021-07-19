from django.db import models
from .utils import uuid_name_upload_to, compress
from user.models import User
from core.models import *
import json
from django.shortcuts import get_object_or_404


class Contact(PostBase):

    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)

    file_attach = models.FileField()
    location = models.ForeignKey(
        to=Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    pay_negotiation = models.BooleanField(default=False)
    free = models.BooleanField(default=False)

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
