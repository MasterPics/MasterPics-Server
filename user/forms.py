from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


# local signup
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('is_ToS', 'nickname', 'username',)

# local login
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("nickname", "password",)
        widgets = {"password": forms.PasswordInput}


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