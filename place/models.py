from django.db import models
from core.models import *

from core.utils import uuid_name_upload_to
from django.shortcuts import get_object_or_404


class Place(PostBase):
    # common field
    user = models.ForeignKey(
        to=User, related_name="places", on_delete=models.CASCADE)

    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    free = models.BooleanField(default=False)

    def to_json(self):
        return {
            'user': self.user,
            'thumbnail': self.thumbnail.url,
            'title': self.title,
            'location': self.location,
            'lat': self.location.lat,
            'lon': self.location.lon,
            'pay': self.location.pay,
            'tag_str': ' '.join([tag.tag for tag in self.tags.all()])
        }
