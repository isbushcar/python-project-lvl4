from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from task_manager.apps.tasks.forms import CreateTaskForm, UpdateTaskForm
from task_manager.apps.users.user_testers import UserIsAuthorOrAdmin
from task_manager.filters import TaskFilter
from task_manager.models import Task
from task_manager.shared_mixin_classes import CustomLoginRequiredMixin, MessageSender


class TasksView(CustomLoginRequiredMixin, FilterView):
    template_name = 'task_manager/tasks/tasks.html'
    context_object_name = 'tasks_list'
    filterset_class = TaskFilter


class UpdateTaskView(CustomLoginRequiredMixin, MessageSender, generic.UpdateView):
    form_class = UpdateTaskForm
    template_name = 'task_manager/tasks/update_task.html'
    model = Task
    success_message = _('Task successfully updated')


class CreateTaskView(CustomLoginRequiredMixin, MessageSender, generic.CreateView):
    form_class = CreateTaskForm
    template_name = 'task_manager/tasks/create_task.html'
    model = Task
    success_message = _('Task successfully сreated')

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class DeleteTaskView(
    CustomLoginRequiredMixin,
    UserIsAuthorOrAdmin,
    MessageSender,
    generic.DeleteView,
):
    template_name = 'task_manager/tasks/delete_task.html'
    model = Task
    no_access_message = _('TaskCanOnlyBeDeletedByItsOwner')
    no_access_redirect_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')


class DetailTaskView(CustomLoginRequiredMixin, generic.DetailView):
    template_name = 'task_manager/tasks/task_detail.html'
    context_object_name = 'task'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Task
        return model.objects.filter(pk=self.kwargs['pk'])
