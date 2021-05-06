import os
from uuid import uuid4
from django.utils import timezone


def uuid_name_upload_to(instance, filename):
    app_label = instance.__class__._meta.app_label  # 앱 별로
    cls_name = instance.__class__.__name__.lower()  # 모델 별로
    ymd_path = timezone.now().strftime('%Y/%m/%d')  # 업로드하는 년/월/일 별로
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return '/'.join([
        app_label,
        cls_name,
        ymd_path,
        uuid_name[:2],
        uuid_name + extension,
    ])


def hashtag_splitter(tag_string):
    return [t.strip() for t in tag_string.split('#') if t.strip()]


def hashtag_joiner(tags):
    return '#' + ' #'.join(t.name for t in tags).lstrip()
