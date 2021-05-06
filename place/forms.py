from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):

    class Meta:
        model = Place
        fields = ('thumbnail', 'title', 'desc', 'pay')

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control place place-title',
                    'id': 'place-title',
                    'placeholder': ''
                }
            ),
            'desc': forms.Textarea(
                attrs={'class': 'form-control place place-desc',
                       'id': 'place-desc',
                       }
            ),
            # 'pay': forms.IntegerField(
            #     attrs={
            #         'class': 'form-control place place-pay',
            #         'id': 'place-pay',
            #     }
            # ),
        }
        labels = {
            'thumbnail': 'Thumbnail',
            'title': 'Title',
            'desc': 'Description',
            'pay': 'Payment',
            'tag_str': 'Hashtag',
        }

        required = {
            'thumbnail': True,
            'title': True,
            'desc': True,
            'pay': True,
        }
