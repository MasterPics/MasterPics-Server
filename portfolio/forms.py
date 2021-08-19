from django import forms
from .models import *
from taggit.forms import TagField, TagWidget


class PortfolioForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, }),required=False)  # 다중이미지
    #required=False는 기존이미지만 제거하는경우때문에

    class Meta:
        model = Portfolio
        fields = ('title',  'desc', 'tags',)
        labels = {
            'title': '제목',
            'desc': '설명',
            'tags': '태그 (#을 붙이고 공백으로 구분)'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'desc': forms.Textarea(
                attrs={'placeholder': '설명을 작성하세요.'}),
            'tags' : TagWidget(
                attrs={
                    'placeholder': '#masterpics #portfolio'}
            ),
        }
