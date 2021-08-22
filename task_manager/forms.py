from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(label=_("First name"),)
    last_name = forms.CharField(label=_("Last name"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class DeleteUserForm(forms.Form):

    class Meta:
        model = User


class UpdateUserForm(ModelForm):
    first_name = forms.CharField(label=_("First name"),)
    last_name = forms.CharField(label=_("Last name"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user