from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic, View

from task_manager.forms import CreateUserForm, UpdateUserForm, CreateStatusForm, UpdateStatusForm
from task_manager.models import Status


class IndexView(View):

    def get(self, request):
        template = loader.get_template('task_manager/index.html')
        context = {
            'page_title': 'Hello, world!',
        }
        return HttpResponse(template.render(context, request))


# --------------- Users Views ---------------

class UsersView(generic.ListView):
    template_name = 'task_manager/users.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        """
        Return list with all users.
        """
        model = get_user_model()
        return model.objects.all()


class CreateUserView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'task_manager/create_user.html'

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


class UpdateUserView(generic.UpdateView):
    form_class = UpdateUserForm
    template_name = 'task_manager/update_user.html'
    model = get_user_model()

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserUpdatedMessage'))
        return reverse_lazy('users_list')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(UpdateUserView, self).get(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] or self.request.user.is_superuser:
            return super(UpdateUserView, self).post( request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return redirect(reverse_lazy('users_list'))


class DeleteUserView(generic.DeleteView):
    template_name = 'task_manager/delete_user.html'
    model = get_user_model()

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserDeletedMessage'))
        return reverse_lazy('users_list')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(DeleteUserView, self).get(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        if self.request.user.id == self.kwargs['pk'] or self.request.user.is_superuser:
            return super(DeleteUserView, self).post(request, *args, **kwargs)
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return redirect(reverse_lazy('users_list'))


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
    template_name = 'task_manager/statuses.html'
    context_object_name = 'statuses_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Status
        return model.objects.all()

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')


class UpdateStatusView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateStatusForm
    template_name = 'task_manager/update_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusUpdatedMessage'))
        return reverse_lazy('statuses')


class CreateStatusView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/create_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusCreatedMessage'))
        return reverse_lazy('statuses')


class DeleteStatusView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/delete_status.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse_lazy('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('StatusDeletedMessage'))
        return reverse_lazy('statuses')
