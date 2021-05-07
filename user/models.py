from django.db import models
from core.utils import uuid_name_upload_to, save_image_from_url
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib


# User field
from phone_field import PhoneField


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

    nickname = models.CharField(max_length=20, unique=True)     # userID
    username = models.CharField(max_length=20, unique=False)    # user 이름
    email = models.EmailField('email address', unique=True)     # social login 시 사용
    category = models.CharField(max_length=20, choices=CATEGORY)
    image = models.ImageField(upload_to=uuid_name_upload_to, blank=True, default='unnamed.png')
    desc = models.TextField(blank=True)
    phone = PhoneField(blank=True)
    phone_public = models.BooleanField(default=False)
    instagram = models.CharField(max_length=20, blank=True)
    is_ToS = models.BooleanField(default=False, validators=[is_ToS])

    # TODO : user_identifier 추가

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['username',]

    # objects = MyUserManager()

    def __str__(self):
        return self.nickname 

