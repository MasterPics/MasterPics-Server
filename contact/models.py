from django.db import models
from .utils import uuid_name_upload_to, compress
from user.models import User
from core.models import Location, Comment, Information, Images
import json
from django.shortcuts import get_object_or_404

# for hashtag
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedContact(TaggedItemBase):
    content_object = models.ForeignKey('Contact', on_delete=models.CASCADE)
    tags = models.ForeignKey(
        'core.Tag', related_name='tagged_contacts', on_delete=models.CASCADE, null=True)


class Contact(models.Model):
    # common field
    user = models.ForeignKey(
        to=User, related_name="contacts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to=uuid_name_upload_to, verbose_name="Image")
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

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    tags = TaggableManager(
        verbose_name='tags', help_text='해시태그를 입력해주세요', blank=True, through=TaggedContact)

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

    def save(self, *args, **kwargs):
        compressed_img = compress(self.thumbnail)
        self.thumbnail = compressed_img
        super().save(*args, **kwargs)


class ContactComment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    @classmethod
    def get_comments(cls, contact):
        try:
            contactComments = ContactComment.objects.filter(contact=contact)
            comments = []
            for contactComment in contactComments:
                comments.append(contactComment.comment)
        except:
            comments = None
        finally:
            return comments


class ContactInformation(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    information = models.OneToOneField(
        Information, related_name='contactInformations', on_delete=models.CASCADE)

class ContactImages(models.Model):
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    contact = models.ForeignKey(to=Contact, null=True, blank=True,
                                  related_name='contact_images', on_delete=models.CASCADE)
