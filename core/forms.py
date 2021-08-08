from django import forms
from .models import Location, PostImage  

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = {'image',}

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('address', 'lat', 'lon',)
        # exclude = ('start_date_time', 'end_date_time',)
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control location location-address',
                       'id': 'location-address',
                       'style': 'width:100%; margin:0 auto;',
                       'placeholder': '주소를 입력하세요.(OO시 OO구 OO동 상세주소)'} #placeholder 추가.
            ),
            'lat': forms.TextInput(
                attrs={'class': 'form-control location location-lat',
                       'id': 'location-lat',
                       'style': 'width:30%;'}
            ),
            'lon': forms.TextInput(
                attrs={'class': 'form-control location location-lon',
                       'id': 'location-lon',
                       'style': 'width:30%;'}
            ),
        }
        labels = {
            'address': '도로명 주소',
            'lat': 'latitude',
            'lon': 'longitude',
        }
        required = {
            # 'address':True,
            # 'lat':True,
            # 'lon':True,
        }