from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from task_manager.apps.tasks.forms import CreateTaskForm, UpdateTaskForm
from task_manager.filters import TaskFilter
from task_manager.models import Task
from task_manager.apps.users.user_testers import UserIsAuthorOrAdmin


class TasksView(LoginRequiredMixin, FilterView):
    template_name = 'task_manager/tasks/tasks.html'
    context_object_name = 'tasks_list'
    filterset_class = TaskFilter

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')


class UpdateTaskView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateTaskForm
    template_name = 'task_manager/tasks/update_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Task successfully updated'))
        return reverse('tasks')


class CreateTaskView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateTaskForm
    template_name = 'task_manager/tasks/create_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Task successfully сreated'))
        return reverse('tasks')

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class DeleteTaskView(LoginRequiredMixin, UserIsAuthorOrAdmin, generic.DeleteView):
    template_name = 'task_manager/tasks/delete_task.html'
    model = Task
    no_access_message = _('TaskCanOnlyBeDeletedByItsOwner')
    no_access_redirect_url = reverse_lazy('tasks')

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Task successfully deleted'))
        return reverse('tasks')


class DetailTaskView(LoginRequiredMixin, generic.DetailView):
    template_name = 'task_manager/tasks/task_detail.html'
    context_object_name = 'task'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Task
        return model.objects.filter(pk=self.kwargs['pk'])

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')
