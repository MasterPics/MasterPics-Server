import os
from uuid import uuid4
from django.utils import timezone
import math

import requests
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from io import BytesIO
from PIL import Image
from django.core.files import File
# from .models import Tag

# models.py에도 utils가 import 돼 있어 순환참조
# Tag 따로 안쓰길래 주석처리함
#from .models import Tag

def compress(image):

    img = Image.open(image)
    img = img.convert('RGB')
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=30)
    compressed_img = File(img_io, name=image.name)
    return compressed_img


def list_to_four_groups(queryset_list):
    l_zero = []
    l_one = []
    l_two = []
    l_three = []
    for idx, val in enumerate(queryset_list):
        if idx % 4 == 0:
            l_zero.append(val)
        elif idx % 4 == 1:
            l_one.append(val)
        elif idx % 4 == 2:
            l_two.append(val)
        else:
            l_three.append(val)
    return l_zero, l_one, l_two, l_three


def uuid_name_upload_to(instance, filename):
    #app_label = instance.__class__._meta.app_label  # 앱 별로
    #cls_name = instance.__class__.__name__.lower()  # 모델 별로
    ymd_path = timezone.now().strftime('%Y/%m/%d')  # 업로드하는 년/월/일 별로
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return '/'.join([
        ymd_path,
        uuid_name,
        uuid_name + extension,
    ])



def save_image_from_url(user, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    user.image.save(uuid_name_upload_to(user, user.email),
                    File(img_temp), save=True)



def hashtag_splitter(tag_string):
    return [t.strip() for t in tag_string.split('#') if t.strip()]


def hashtag_joiner(tags):
    if tags:
        return '#' + ' #'.join(t.name for t in tags).lstrip()
    else:
        return ''
