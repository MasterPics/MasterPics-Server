from django import forms
from .models import *


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('title', 'thumbnail',  'desc', 'tag_str',)

    def __init__(self, *args, **kwargs):
        super(PortfolioForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({
                'class': field + " form",
                'id': 'form-id', })
