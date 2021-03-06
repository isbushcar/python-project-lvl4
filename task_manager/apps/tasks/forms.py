from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.models import Label, Status, Task, User


class CreateTaskForm(ModelForm):
    name = forms.CharField(
        label=_('Name'),
        error_messages={'unique': _('TaskAlreadyExists')},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'label': _('Description'),
                'rows': 10,
                'cols': 40,
                'class': 'form-control',
                'placeholder': _('Description'),
            },
        ),
        required=False,
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        empty_label=_('ChooseStatus'),
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        empty_label=_('ChooseExecutor'),
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label=_('Labels'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
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
