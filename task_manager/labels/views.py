from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from task_manager.mixins import FailureMessageMixin
from task_manager.users.mixins import AuthRequireMixin
from .models import Label


class IndexView(FailureMessageMixin, AuthRequireMixin, ListView):
    model = Label
    context_object_name = 'labels'
    fields = ['id', 'name']
    template_name = 'labels/index.html'


class CreateLabelView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Label
    fields = ['name']
    template_name = 'labels/create.html'
    success_message = _('Метка успешна создана')
    success_url = reverse_lazy('labels:index')


class UpdateLabelView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Label
    fields = ['name']
    template_name = 'labels/update.html'
    success_message = _('Метка успешна обновлена')
    success_url = reverse_lazy('labels:index')


class DeleteLabelView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Label
    template_name = 'labels/delete.html'
    success_message = _('Метка успешна удалена')
    success_url = reverse_lazy('labels:index')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(self.request, 'Метка используется, нельзя удалить')
            return redirect('labels:index')
