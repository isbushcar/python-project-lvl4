from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.apps.labels.forms import CreateLabelForm
from task_manager.models import Label, Status, Task
from task_manager.shared_mixin_classes import CustomLoginRequiredMixin, SendMessageMixin


class LabelsView(CustomLoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/labels/labels.html'
    context_object_name = 'labels_list'
    permission_denied_message = _('NeedToLogInFirst')

    def get_queryset(self):
        model = Label
        return model.objects.all()


class UpdateLabelView(CustomLoginRequiredMixin, SendMessageMixin, generic.UpdateView):
    form_class = CreateLabelForm
    template_name = 'task_manager/labels/update_label.html'
    model = Label
    success_message = _('Label successfully updated')


class CreateLabelView(CustomLoginRequiredMixin, SendMessageMixin, generic.CreateView):
    form_class = CreateLabelForm
    template_name = 'task_manager/labels/create_label.html'
    model = Status
    success_message = _('Label successfully created')


class DeleteLabelView(CustomLoginRequiredMixin, SendMessageMixin, generic.DeleteView):
    template_name = 'task_manager/labels/delete_label.html'
    model = Label
    success_message = _('Label successfully deleted')

    def delete(self, request, *args, **kwargs):
        if Task.objects.filter(labels=self.kwargs['pk']).exists():
            self.success_message = _('YouCantDeleteLabelThatIsUsedInTask')
            success_url = self.get_success_url()
            return redirect(success_url)
        success_url = self.get_success_url()
        self.get_object().delete()
        return redirect(success_url)
