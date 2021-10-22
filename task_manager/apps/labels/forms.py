from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.models import Label


class CreateLabelForm(ModelForm):
    name = forms.CharField(
        label=_('Name'),
        error_messages={'unique': _('LabelAlreadyExists')},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
    )

    def __init__(self, *args, **kwargs):
        super(CreateLabelForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Label
        fields = ('name', )
