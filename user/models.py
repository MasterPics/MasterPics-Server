from django.db import models
from core.utils import uuid_name_upload_to, save_image_from_url
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib

#For Hashing Password
from hashid_field import HashidField, HashidAutoField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable
 

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

    user_id = models.CharField(max_length=20, unique=True, verbose_name='아이디')     # user id
    username = models.CharField(max_length=20, unique=False, verbose_name='사용자 이름')    # user name (본명 혹은 예명)
    email = models.EmailField(unique=True, verbose_name='이메일')
    email_public = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default='otheruse')
    image = models.ImageField(upload_to=uuid_name_upload_to, blank=True, default='unnamed.png')
    desc = models.TextField(blank=True, verbose_name='프로필 소개')
    phone = PhoneField(blank=True)
    phone_public = models.BooleanField(default=True)
    instagram = models.CharField(max_length=20, blank=True)
    instagram_public = models.BooleanField(default=True)
    is_ToS = models.BooleanField(default=False, validators=[is_ToS])
    is_social = models.BooleanField(default=False)
    user_identifier = models.CharField(max_length=100, blank=True, null=True)
    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username', 'email',]

    # objects = MyUserManager()

    def __str__(self):
        return self.user_id 


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)