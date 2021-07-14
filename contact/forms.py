from django import forms
from .models import *

# form validator
from django.core.exceptions import ValidationError
import datetime


class ContactForm(forms.ModelForm):
    # 해당 모델 자체의 정보를 담는 네임스페이스 클래스
    # https://stackoverflow.com/questions/57241617/what-is-exactly-meta-in-django
    images = forms.ImageField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}))  # 다중이미지
            
    class Meta:

        model = Contact
        fields = ('title', 'desc', 'start_date', 'end_date', 
                  'file_attach', 'pay', 'tags')
        widgets = {
            'start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({
                'class': field + " form",
                'id': 'form-id', })

    def clean(self):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        if start_date.date() < datetime.date.today():
            self._errors['start_date'] = self.error_class(
                ['시작일은 오늘보다 빠를 수 없습니다.'])

        if end_date < start_date:
            self._errors['end_date'] = self.error_class(
                ['종료일은 시작일보다 빠를 수 없습니다.'])

        return self.cleaned_data
