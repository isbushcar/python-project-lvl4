from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic, View

from task_manager.forms import CreateUserForm, UpdateUserForm, CreateStatusForm, CreateTaskForm, UpdateTaskForm
from task_manager.models import Status, Task


class UserIsOwnerOrAdmin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.id == self.kwargs['pk'] or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            self.no_access_message += '. ' + _('TryToLoginFirst')
        messages.add_message(self.request, messages.INFO, self.no_access_message)
        return redirect(self.no_access_redirect_url)
