from django.db import models
from core.utils import uuid_name_upload_to, save_image_from_url
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import urllib

# For Hashing Password
from hashid_field import HashidField, HashidAutoField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable


# User field
from phone_field import PhoneField

# User validators
from django import forms
from django.core.exceptions import ValidationError

# User image uuid-upload
from .utils import user_uuid_name_upload_to

# For UserManager
from django.contrib.auth.models import BaseUserManager
import time
import hashlib


class UserManager(BaseUserManager):    
    use_in_migrations = True
    
    def create_user(self, user_id, username, email, password=None):
        if not email :
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            user_id=user_id,
            username=username,
        )        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, user_id, username, email,password ):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            user_id=user_id,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        
        # hash (add user_identifier)
        string = str(user.pk + int(time.time()))
        encoded_string = string.encode()
        result = hashlib.sha256(encoded_string).hexdigest()
        user.user_identifier = result

        user.is_ToS = True
        user.save(using=self._db)

        return user 


# User validators 
def is_ToS(value):
    if value == False:
        raise forms.ValidationError("약관에 동의해야 합니다.")


class User(AbstractUser):
    objects = UserManager()

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

    user_id = models.CharField(max_length=20, verbose_name='아이디')     # user id
    username = models.CharField(max_length=20, unique=False, verbose_name='사용자 이름')    # user name (본명 혹은 예명)
    email = models.EmailField(unique=True, verbose_name='이메일')
    email_public = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default='otheruse')
    image = models.ImageField(upload_to=user_uuid_name_upload_to, blank=True, default='user/profile_photo/default/profile_default.png')
    desc = models.TextField(blank=True, verbose_name='프로필 소개')
    phone = PhoneField(blank=True)
    phone_public = models.BooleanField(default=True)
    instagram = models.CharField(max_length=20, blank=True)
    instagram_public = models.BooleanField(default=True)
    is_ToS = models.BooleanField(default=False, validators=[is_ToS])
    is_social = models.BooleanField(default=False)
    user_identifier = models.CharField(max_length=100, blank=True, null=True)
    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True, blank=True)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username', 'email', ]


    def __str__(self):
        return self.username

    def clean(self, *args, **kwargs):
        user_id = self.user_id

        # social signup 시의 오류 해결
        if user_id == '':
            return
        
        # profile modify 시의 오류 해결
        user_id_same_users = User.objects.filter(user_id=user_id)
        current_user = self.pk
        for user in user_id_same_users:
            if user.pk == current_user:
                return
        
        if User.objects.filter(user_id=user_id).exists():
            raise ValidationError({
                'user_id': ValidationError('이미 존재하는 아이디입니다.')
            })


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)
