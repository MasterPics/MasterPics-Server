from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))  # 다중이미지

    class Meta:
        model = Place
        fields = ('thumbnail', 'title', 'desc', 'pay')
