from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.apps.statuses.forms import CreateStatusForm
from task_manager.models import Status
from task_manager.shared_mixin_classes import CustomLoginRequiredMixin, MessageSender


class StatusesView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/statuses/statuses.html'
    context_object_name = 'statuses_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Status
        return model.objects.all()


class UpdateStatusView(CustomLoginRequiredMixin, MessageSender, generic.UpdateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/update_status.html'
    model = Status
    success_message = _('Status successfully updated')


class CreateStatusView(CustomLoginRequiredMixin, MessageSender, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/create_status.html'
    model = Status
    success_message = _('Status successfully created')


class DeleteStatusView(CustomLoginRequiredMixin, MessageSender, generic.DeleteView):
    template_name = 'task_manager/statuses/delete_status.html'
    model = Status
    success_message = _('Status successfully deleted')

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
