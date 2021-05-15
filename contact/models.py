from django.db import models
from .utils import uuid_name_upload_to
from user.models import User
from core.models import Location, Comment, Information, Images
import json
from django.shortcuts import get_object_or_404


#TODO Contact 이미지 하기
class Contact(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)
    thumbnail = models.ForeignKey(Images, related_name="contact_thumbnail", on_delete=models.CASCADE, blank=True, null=True, default=None)
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()

    # specific field
    file_attach = models.FileField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, blank=True)
    pay = models.PositiveIntegerField()
    pay_negotiation = models.BooleanField(default=False)
    free = models.BooleanField(default=False)

    # TODO decorator 추가하기 지민아 화이팅
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

class ContactComment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    @classmethod
    def get_comments(cls, contact):
        try:
            comments = ContactComment.objects.filter(contact=contact)
        except:
            comments = None
        finally:
            return comments

class ContactInformation(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, on_delete=models.CASCADE)
