from django import forms
from .models import Place
from taggit.forms import TagWidget


class PlaceForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'placeholder': '이미지 파일을 등록하세요.'}))  # 다중이미지

    class Meta:
        model = Place
        fields = ('title', 'pay', 'tags', 'desc')
        # 순서 변경
        # 동시에 상호무페이랑 pay를 처리하는 것 보다는 전에 했던 대로 가격이 0인 경우 상호무페이 처리가 간결한 것 같아서 다시 수정했습니다.
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'pay': forms.NumberInput(attrs={'placeholder': '페이를 입력하세요.(상호 무페이의 경우 0을 입력하세요)'}),
            'tags' : TagWidget(
                attrs={
                    'placeholder': '#masterpics #portfolio'}
            ),
            'desc': forms.Textarea(attrs={'placeholder': '상세 설명을 작성하세요.'})
        }
        # placeholder 위젯 적용
        # 요청사항 : lat,lon 속성 null 허용해주세요!
