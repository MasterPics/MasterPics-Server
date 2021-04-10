from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'category',
                  'image', 'desc',)
        excldue = ('password', )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        print(self.fields.keys(), type(self.fields.keys()))
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({
                'class': field + " form",
                'id': 'form-id', })


class SocialSignUpForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'category', 'image', 'desc',)
        # excldue = ('password', )
