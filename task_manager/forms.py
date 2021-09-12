from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

from task_manager.models import Status, Task


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
        label=_("Name"),
        error_messages={'unique': _("StatusAlreadyExists")}
    )

    class Meta:
        model = Status
        fields = ('name', )


class CreateTaskForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        error_messages={'unique': _("TaskAlreadyExists")},
        widget=forms.TextInput(attrs={"class":"form-control"}),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'label': _("Description"), 'rows': 10, 'cols': 40, "class": "form-control"},
        ),
        required=False,
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        empty_label=_("ChooseStatus"),
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_("Executor"),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
        empty_label=_("ChooseExecutor"),
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'author', 'executor')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        if self.current_user is not None:
            self.fields['author'] = forms.ModelChoiceField(
                queryset=User.objects.filter(pk=self.current_user.id),
                required=True,
                initial=self.current_user,
            )


class UpdateTaskForm(CreateTaskForm):

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor')
