from django.db import models
from core.models import Location, Comment, Information
from user.models import User
from core.utils import uuid_name_upload_to

# Create your models here.


class Place(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="posts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()

    # specific field
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    # fee
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
            'tag_str': ' '.join([tag.tag for tag in tags.all()])
        }


class PlaceComment(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class PlaceInformation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
