from django import forms
from .models import *


class PortfolioForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, }))  # 다중이미지

    class Meta:
        model = Portfolio
        fields = ('title',  'desc', 'tags',)
        labels = {
            'title': '제목',
            'desc': '설명',
            'tags': '태그 (#을 붙이고 공백으로 구분)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            'desc': forms.Textarea(
                attrs={'placeholder': '설명을 작성하세요.'}),
            'tags': forms.TextInput(attrs={'placeholder': '#masterpics #portfolio'}),
        }
