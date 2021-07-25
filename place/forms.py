from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'placeholder': '이미지 파일을 등록하세요.'}))  # 다중이미지

    class Meta:
        model = Place
        fields = ('title', 'pay', 'tags', 'desc')
        # 순서 변경ㅋ
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'pay': forms.NumberInput(attrs={'placeholder': '페이를 입력하세요.(상호 무페이의 경우 0을 입력하세요)'}),
            'tags': forms.TextInput(attrs={'placeholder': '해시태그를 입력하세요.'}),
            'desc': forms.Textarea(attrs={'placeholder': '상세 설명을 작성하세요.'})
        }
        # placeholder 위젯 적용
        # 요청사항 : lat,lon 속성 null 허용해주세요!
