from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.apps.users.fields import UsernameFieldWithPlaceholder
from task_manager.apps.users.models import User


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First name')}),
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last name')}),
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
                'class': 'form-control',
            }
        )
        self.fields['password1'].help_text = _(
            'Password should contain at least 8 characters'
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': _('Password confirmation'),
                'class': 'form-control',
            }
        )
        self.label_suffix = ''

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        field_classes = {'username': UsernameFieldWithPlaceholder}


class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(request=request, *args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': _('UserName'),
        })
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': _('Password'),
            }
        )
        self.label_suffix = ''
