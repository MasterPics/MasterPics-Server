from django import forms
from .models import *


class ContactForm(forms.ModelForm):
    # 해당 모델 자체의 정보를 담는 네임스페이스 클래스
    # https://stackoverflow.com/questions/57241617/what-is-exactly-meta-in-django
    class Meta:
        model = Contact
        fields = ('title', 'desc', 'start_date', 'end_date', 'thumbnail',
                  'file_attach', 'pay')
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
