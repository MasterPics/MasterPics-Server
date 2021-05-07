from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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


# social signup 시 redirect page에서 추가로 입력받아야 할 정보를 담은 form
class SocialSignUpForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'category', 'image', 'desc', 'phone', 'phone_public', 'instagram', 'is_ToS')
        # excldue = ('password', )


# local signup
class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'is_ToS', 'category',)