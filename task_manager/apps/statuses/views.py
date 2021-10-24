from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.apps.statuses.forms import CreateStatusForm
from task_manager.models import Status, Task
from task_manager.shared_mixin_classes import CustomLoginRequiredMixin, SendMessageMixin


class StatusesView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/statuses/statuses.html'
    context_object_name = 'statuses_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Status
        return model.objects.all()


class UpdateStatusView(CustomLoginRequiredMixin, SendMessageMixin, generic.UpdateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/update_status.html'
    model = Status
    success_message = _('Status successfully updated')


class CreateStatusView(CustomLoginRequiredMixin, SendMessageMixin, generic.CreateView):
    form_class = CreateStatusForm
    template_name = 'task_manager/statuses/create_status.html'
    model = Status
    success_message = _('Status successfully created')


class DeleteStatusView(CustomLoginRequiredMixin, SendMessageMixin, generic.DeleteView):
    template_name = 'task_manager/statuses/delete_status.html'
    model = Status
    success_message = _('Status successfully deleted')

    def delete(self, request, *args, **kwargs):
        if Task.objects.filter(status=self.kwargs['pk']):
            self.success_message = _('YouCantDeleteStatusThatIsUsedInTask')
            success_url = self.get_success_url()
            return redirect(success_url)
        success_url = self.get_success_url()
        self.get_object().delete()
        return redirect(success_url)
