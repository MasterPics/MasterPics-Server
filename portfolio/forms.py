from django import forms
from .models import *


class PortfolioForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))  # 다중이미지

    class Meta:
        model = Portfolio
        fields = ('title', 'thumbnail',  'desc', 'tag_str', 'images')