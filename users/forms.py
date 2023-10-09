from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

from users.models import User
from django import forms


class MixinForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserCreationForm(MixinForm, BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserUpdateForm(MixinForm, BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
