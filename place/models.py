from django.db import models
from core.models import *
from user.models import User
from core.utils import uuid_name_upload_to
from django.shortcuts import get_object_or_404

# for hashtag
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedPlace(TaggedItemBase):
    content_object = models.ForeignKey('Place', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'core.Tag', related_name='tagged_places', on_delete=models.CASCADE, null=True)


class Place(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="places", on_delete=models.CASCADE)
    thumbnail = models.ForeignKey(Images, related_name="place_thumbnail",
                                  on_delete=models.CASCADE, blank=True, null=True, default=None)
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

    tags = TaggableManager(
        verbose_name='tags', help_text='해시태그를 입력해주세요', blank=True, through=TaggedPlace)

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

    @classmethod
    def get_comments(cls, target):
        try:
            comments = PlaceComment.objects.filter(place=target)
        except:
            comments = None
        finally:
            return comments


class PlaceInformation(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    information = models.OneToOneField(Information, on_delete=models.CASCADE)


# TODO place는 attached files
class PlaceImages(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    place = models.ForeignKey(to=Place, null=True, blank=True,
                              related_name='place_images', on_delete=models.CASCADE)
