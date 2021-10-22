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
from task_manager.forms import CreateUserForm, UserAuthenticationForm
from task_manager.models import Label, Status, Task


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
        model = get_user_model()
        return model.objects.all()


class CreateUserView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'task_manager/users/create_user.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('User successfully created'))
        return reverse('login')

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, _('AlreadyInMessage'))
            return redirect(reverse('users_list'))
        return super(CreateUserView, self).post(request, *args, **kwargs)


class UpdateUserView(UserIsUserHimselfOrAdmin, generic.UpdateView):
    form_class = CreateUserForm
    template_name = 'task_manager/users/update_user.html'
    model = get_user_model()
    no_access_message = _('YouCantUpdateOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        update_session_auth_hash(
            self.request,
            *get_user_model().objects.filter(pk=self.request.user.pk),
        )
        messages.add_message(self.request, messages.INFO, _('User successfully updated'))
        return reverse('users_list')


class DeleteUserView(UserIsUserHimselfOrAdmin, generic.DeleteView):
    template_name = 'task_manager/users/delete_user.html'
    model = get_user_model()
    no_access_message = _('YouCantDeleteOtherUsers')
    no_access_redirect_url = reverse_lazy('users_list')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('User successfully deleted'))
        return reverse('users_list')


class UserLoginView(LoginView):
    template_name = 'task_manager/login.html'
    form_class = UserAuthenticationForm

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedInMessage'))
        return reverse('main_page')


class UserLogoutView(LogoutView):

    def get_next_page(self):
        messages.add_message(self.request, messages.INFO, _('UserLoggedOutMessage'))
        return reverse('main_page')




