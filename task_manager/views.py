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
from task_manager.custom_helper_classes import UserIsOwnerOrAdmin


class IndexView(View):

    def get(self, request):
        template = loader.get_template('task_manager/index.html')
        context = {
            'page_title': 'Hello, world!',
        }
        return HttpResponse(template.render(context, request))


# --------------- Users Views ---------------

class UsersView(generic.ListView):
    template_name = 'task_manager/users/users.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        """
        Return list with all users.
        """
        model = get_user_model()
        return model.objects.all()


class CreateUserView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'task_manager/users/create_user.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserCreatedMessage'))
        return reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('AlreadyInMessage'))
            return redirect(reverse_lazy('users_list'))
        return super(CreateUserView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('AlreadyInMessage'))
            return redirect(reverse_lazy('users_list'))
        return super(CreateUserView, self).post(request, *args, **kwargs)


class UpdateUserView(UserIsOwnerOrAdmin, generic.UpdateView):
    form_class = UpdateUserForm
    template_name = 'task_manager/users/update_user.html'
    model = get_user_model()
    no_access_message = _('YouCantUpdateOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserUpdatedMessage'))
        return reverse_lazy('users_list')


class DeleteUserView(UserIsOwnerOrAdmin, generic.DeleteView):
    template_name = 'task_manager/users/delete_user.html'
    model = get_user_model()
    no_access_message = _('YouCantDeleteOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserDeletedMessage'))
        return reverse_lazy('users_list')


class UserLoginView(LoginView):
    template_name = 'task_manager/login.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedInMessage'))
        return reverse_lazy('users_list')


class UserLogoutView(LogoutView):

    def get_next_page(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedOutMessage'))
        return reverse_lazy('main_page')


# --------------- Statuses Views ---------------

class StatusesView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/statuses/statuses.html'
    context_object_name = 'statuses_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Status
        return model.objects.all()

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')


class UpdateStatusView(LoginRequiredMixin, generic.UpdateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/update_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusUpdatedMessage'))
        return reverse_lazy('statuses')


class CreateStatusView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/create_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusCreatedMessage'))
        return reverse_lazy('statuses')


class DeleteStatusView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/statuses/delete_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusDeletedMessage'))
        return reverse_lazy('statuses')


# --------------- Tasks Views ---------------

class TasksView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/tasks/tasks.html'
    context_object_name = 'tasks_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Task
        return model.objects.all()

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')


class UpdateTaskView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateTaskForm
    template_name = 'task_manager/tasks/update_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('TaskUpdatedMessage'))
        return reverse_lazy('tasks')


class CreateTaskView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateTaskForm
    template_name = 'task_manager/tasks/create_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('TaskCreatedMessage'))
        return reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super(CreateTaskView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class DeleteTaskView(LoginRequiredMixin, UserIsOwnerOrAdmin, generic.DeleteView):
    template_name = 'task_manager/tasks/delete_task.html'
    model = Task
    no_access_message = _('TaskCanOnlyBeDeletedByItsOwner')
    no_access_redirect_url = reverse_lazy('tasks')

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('TaskDeletedMessage'))
        return reverse_lazy('tasks')


class DetailTaskView(generic.DetailView):
    template_name = 'task_manager/tasks/task_detail.html'
    context_object_name = 'task'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Task
        return model.objects.filter(pk=self.kwargs['pk'])

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

