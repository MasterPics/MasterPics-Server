from django.db import models
from django_mysql.models import ListCharField
from user.models import User
from .utils import uuid_name_upload_to


# Reference tab does not use additional modelsp