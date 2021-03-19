from django.db import models
from core.models import Tag, Location
from user.models import User

# Create your models here.
class Place(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="posts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=uuid_name_upload_to)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    save_users = models.ManyToManyField(
        to=User, related_name='save_users', blank=True)
    desc = models.TextField()

    # specific field
    like_users = models.ManyToManyField(
        to=User, related_name='like_users', blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    tag_str = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag, related_name='places', blank=True)

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