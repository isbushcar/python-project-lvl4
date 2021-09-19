from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic, View

from task_manager.forms import CreateUserForm, UpdateUserForm, CreateStatusForm, CreateTaskForm, UpdateTaskForm,\
    CreateLabelForm
from task_manager.models import Label, Status, Task
from task_manager.custom_helper_classes import UserIsOwnerOrAdmin
from django.db.models import ProtectedError

class IndexView(View):  # TODO: rework

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
        messages.add_message(self.request, messages.INFO, f"{_('User')} {_('successfullyCreated')}")
        return reverse('login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('AlreadyInMessage'))
            return redirect(reverse('users_list'))
        return super(CreateUserView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('AlreadyInMessage'))
            return redirect(reverse('users_list'))
        return super(CreateUserView, self).post(request, *args, **kwargs)


class UpdateUserView(UserIsOwnerOrAdmin, generic.UpdateView):
    form_class = UpdateUserForm
    template_name = 'task_manager/users/update_user.html'
    model = get_user_model()
    no_access_message = _('YouCantUpdateOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('User')} {_('successfullyUpdated')}")
        return reverse('users_list')


class DeleteUserView(UserIsOwnerOrAdmin, generic.DeleteView):
    template_name = 'task_manager/users/delete_user.html'
    model = get_user_model()
    no_access_message = _('YouCantDeleteOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('User')} {_('successfullyDeleted')}")
        return reverse('users_list')


class UserLoginView(LoginView):
    template_name = 'task_manager/login.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedInMessage'))
        return reverse('users_list')


class UserLogoutView(LogoutView):

    def get_next_page(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedOutMessage'))
        return reverse('main_page')


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
        return reverse('login')


class UpdateStatusView(LoginRequiredMixin, generic.UpdateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/update_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Status')} {_('successfullyUpdated')}")
        return reverse('statuses')


class CreateStatusView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/create_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Status')} {_('successfullyCreated')}")
        return reverse('statuses')


class DeleteStatusView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/statuses/delete_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Status')} {_('successfullyDeleted')}")
        return reverse('statuses')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(self.request, messages.INFO, _('YouCantDeleteStatusThatIsUsedInTask'))
            return redirect(reverse('statuses'))
        success_url = self.get_success_url()
        return redirect(success_url)

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
        return reverse('login')


class UpdateTaskView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateTaskForm
    template_name = 'task_manager/tasks/update_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Task')} {_('successfullyUpdated')}")
        return reverse('tasks')


class CreateTaskView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateTaskForm
    template_name = 'task_manager/tasks/create_task.html'
    model = Task

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Task')} {_('successfullyCreated')}")
        return reverse('tasks')

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
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Task')} {_('successfullyDeleted')}")
        return reverse('tasks')


class DetailTaskView(generic.DetailView):
    template_name = 'task_manager/tasks/task_detail.html'
    context_object_name = 'task'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Task
        return model.objects.filter(pk=self.kwargs['pk'])

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['labels_list'] = Label.objects.all()
    #     return context


# --------------- Labels Views ---------------

class LabelsView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/labels/labels.html'
    context_object_name = 'labels_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Label
        return model.objects.all()

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')


class UpdateLabelView(LoginRequiredMixin, generic.UpdateView):
    form_class = CreateLabelForm
    template_name = 'task_manager/labels/update_label.html'
    model = Label

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Label')} {_('successfullyUpdated')}")
        return reverse('labels')


class CreateLabelView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateLabelForm
    template_name = 'task_manager/labels/create_label.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Task')} {_('successfullyCreated')}")
        return reverse('labels')


class DeleteLabelView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/labels/delete_label.html'
    model = Label

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, f"{_('Task')} {_('successfullyDeleted')}")
        return reverse('labels')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(self.request, messages.INFO, _('YouCantDeleteLabelThatIsUsedInTask'))
            return redirect(reverse('labels'))
        success_url = self.get_success_url()
        return redirect(success_url)
