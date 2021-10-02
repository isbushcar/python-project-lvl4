import django_filters
from django import forms
from django.db import models
from django_filters import BooleanFilter, ModelChoiceFilter, ModelMultipleChoiceFilter

from task_manager.models import Label, Status, Task, User


class TaskFilter(django_filters.FilterSet):
    users_tasks_only = BooleanFilter(
        field_name='author',
        method='get_users_tasks_only',
        widget=forms.CheckboxInput
    )
    status = ModelChoiceFilter(
        field_name='status',
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    executor = ModelChoiceFilter(
        field_name='executor',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    labels = ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def get_users_tasks_only(self, queryset, name, value):
        author = getattr(self.request, 'user', None)
        if value is True:
            return queryset.filter(author=author)
        return queryset
