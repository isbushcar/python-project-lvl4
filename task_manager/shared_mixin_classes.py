from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')


class SendMessageMixin:

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, self.success_message)
        if hasattr(self, 'object'):
            return self.object.get_absolute_url()
        return self.get_object().get_absolute_url()
