from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from task_manager.models import Status


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(label=_("First name"),)
    last_name = forms.CharField(label=_("Last name"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


class UpdateUserForm(ModelForm):
    first_name = forms.CharField(label=_("First name"),)
    last_name = forms.CharField(label=_("Last name"),)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CreateStatusForm(ModelForm):
    name = forms.CharField(
        label=_("StatusName"),
        error_messages={'unique': _("StatusAlreadyExists")}
    )

    class Meta:
        model = Status
        fields = ('name', )


class UpdateStatusForm(ModelForm):
    name = forms.CharField(
        label=_("StatusName"),
        error_messages={'unique': _("StatusAlreadyExists")}
    )

    class Meta:
        model = Status
        fields = ('name', )
