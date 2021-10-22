from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.apps.labels.forms import CreateLabelForm
from task_manager.models import Label, Status, Task


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
        messages.add_message(self.request, messages.INFO, _('Label successfully updated'))
        return reverse('labels')


class CreateLabelView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateLabelForm
    template_name = 'task_manager/labels/create_label.html'
    model = Status

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Label successfully created'))
        return reverse('labels')


class DeleteLabelView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'task_manager/labels/delete_label.html'
    model = Label

    def get_login_url(self):
        messages.add_message(self.request, messages.INFO, _('NeedToLogInFirst'))
        return reverse('login')

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, _('Label successfully deleted'))
        return reverse('labels')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Task.objects.filter(labels=self.kwargs['pk']):
            messages.add_message(
                self.request,
                messages.INFO, _('YouCantDeleteLabelThatIsUsedInTask'),
            )
            return redirect(reverse('labels'))
        return super(DeleteLabelView, self).delete(request, *args, **kwargs)
