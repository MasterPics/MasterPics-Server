import os
from uuid import uuid4
from django.utils import timezone

from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image):
    img = Image.open(image)
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=50)
    compressed_img = File(img_io, name=image.name)
    return compressed_img


def uuid_name_upload_to(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d')  # 업로드하는 년/월/일 별로
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return '/'.join([
        ymd_path,
        uuid_name,
        uuid_name + extension,
    ])


def hashtag_splitter(tag_string):
    return [t.strip() for t in tag_string.split('#') if t.strip()]


def hashtag_joiner(tags):
    return '#' + ' #'.join(t.name for t in tags).lstrip()
