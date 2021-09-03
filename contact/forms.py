from django import forms
from .models import *
from taggit.forms import TagWidget

# form validator
from django.core.exceptions import ValidationError
import datetime



class ContactForm(forms.ModelForm):
    # 해당 모델 자체의 정보를 담는 네임스페이스 클래스
    # https://stackoverflow.com/questions/57241617/what-is-exactly-meta-in-django
    images = forms.ImageField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)  # 다중이미지 ,required=False는 기존이미지만 제거하는경우때문에
            
    class Meta:

        model = Contact
        fields = ('title', 'desc', 'start_date', 'end_date', 
                  'file_attach', 'pay_type', 'pay', 'tags')
        labels = {
            'title': '제목',
            'desc': '설명',
            'tags': '태그 (#을 붙이고 공백으로 구분)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '아티스트 섭외를 위한 제목을 입력하세요.'}),
            'desc': forms.Textarea(
                attrs={'placeholder': '사진작업의 컨셉, 요구사항, 섭외할 아티스트 등 사진작업에 대한 구체적인 설명을 입력하세요.'}),
            'tags': forms.TextInput(attrs={'placeholder': '사진작업과 관련된 키워드를 입력하세요. (ex. #masterpics #contact)'}),
            'pay': forms.NumberInput(attrs={'placeholder': '페이입력'}),

            'start_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'end_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
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
