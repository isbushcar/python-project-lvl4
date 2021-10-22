from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic, View
from django_filters.views import FilterView
from django.contrib.auth import update_session_auth_hash

from task_manager.user_testers import UserIsUserHimselfOrAdmin, UserIsAuthorOrAdmin
from task_manager.filters import TaskFilter
from task_manager.apps.statuses.forms import CreateStatusForm
from task_manager.models import Status, Task


class StatusesView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/statuses/statuses.html'
    context_object_name = 'statuses_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Status
        return model.objects.all()

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')


class UpdateStatusView(LoginRequiredMixin, generic.UpdateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/update_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Status successfully updated'))
        return reverse('statuses')


class CreateStatusView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/create_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Status successfully created'))
        return reverse('statuses')


class DeleteStatusView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/statuses/delete_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Status successfully deleted'))
        return reverse('statuses')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(
                self.request,
                messages.INFO, _('YouCantDeleteStatusThatIsUsedInTask'),
            )
            return redirect(reverse('statuses'))
        success_url = self.get_success_url()
        return redirect(success_url)
