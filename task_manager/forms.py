from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.models import Label, Status, Task
from task_manager.fields import UsernameFieldWithPlaceholder


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _('First name')}),
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
        self.fields['password1'].help_text = _('<li>Password should contain at least 8 characters</li>')
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


class CreateStatusForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        error_messages={'unique': _("StatusAlreadyExists")},
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _("Name")}),
    )

    def __init__(self, *args, **kwargs):
        super(CreateStatusForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Status
        fields = ('name', )


class CreateTaskForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        error_messages={'unique': _("TaskAlreadyExists")},
        widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': _("Name")}),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'label': _("Description"),
                'rows': 10,
                'cols': 40,
                "class": "form-control",
                'placeholder': _("Description"),
            },
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
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label=_("Labels"),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'author', 'executor', 'labels')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        if self.current_user is not None:
            self.fields['author'] = forms.ModelChoiceField(
                queryset=User.objects.filter(pk=self.current_user.id),
                required=True,
                initial=self.current_user,
            )


class UpdateTaskForm(CreateTaskForm):

    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')


class CreateLabelForm(ModelForm):
    name = forms.CharField(
        label=_("Name"),
        error_messages={'unique': _("LabelAlreadyExists")},
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _("Name")}),
    )

    def __init__(self, *args, **kwargs):
        super(CreateLabelForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Label
        fields = ('name', )


class UserAuthenticationForm(AuthenticationForm):
    
    def __init__(self, request=None, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(request=request, *args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'autofocus': True, 'placeholder': _('UserName')})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'placeholder': _('Password'),
            }
        )
        self.label_suffix = ''
