from django.db import models
from core.utils import uuid_name_upload_to, save_image_from_url
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib
from hashid_field import HashidField, HashidAutoField


# Create your models here.

# from django.contrib.auth.models import BaseUserManager


# class MyUserManager(BaseUserManager):
#     """
#     A custom user manager to deal with emails as unique identifiers for auth
#     instead of usernames. The default that's used is "UserManager"
#     """

#     def _create_user(self, email, password, **extra_fields):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('The Email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(email, password, **extra_fields)



# ------------------------new--------------------------------

# User field
from phone_field import PhoneField

# User validators 
from django import forms
from django.core.exceptions import ValidationError

# User validators 
def is_ToS(value):
    if value == False:
        raise forms.ValidationError("약관에 동의해야 합니다.")


class User(AbstractUser):
    CATEGORY_PHOTOGRAPHER = 'photographer'
    CATEGORY_MODEL = 'model'
    CATEGORY_HM = 'HairMakeup'
    CATEGORY_STYLIST = 'stylist'
    CATEGORY_OTHERS = 'otheruse'

    CATEGORY = (
        ('photographer', CATEGORY_PHOTOGRAPHER),
        ('model', CATEGORY_MODEL),
        ('HairMakeup', CATEGORY_HM),
        ('stylist', CATEGORY_STYLIST),
        ('otheruse', CATEGORY_OTHERS),
    )

    user_id = models.CharField(max_length=20, unique=True)     # user id
    username = models.CharField(max_length=20, unique=False)    # user name (본명 혹은 예명)
    email = models.EmailField('email address', unique=True)
    email_public = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY)
    image = models.ImageField(upload_to=uuid_name_upload_to, blank=True, default='unnamed.png')
    desc = models.TextField(blank=True)
    phone = PhoneField(blank=True)
    phone_public = models.BooleanField(default=True)
    instagram = models.CharField(max_length=20, blank=True)
    instagram_public = models.BooleanField(default=True)
    is_ToS = models.BooleanField(default=False, validators=[is_ToS])
    is_social = models.BooleanField(default=False)
    user_identifier = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username', 'email',]

    # objects = MyUserManager()

    def __str__(self):
        return self.user_id 

