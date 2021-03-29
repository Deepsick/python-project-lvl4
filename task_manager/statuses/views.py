from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import FailureMessageMixin
from task_manager.users.mixins import AuthRequireMixin
from .models import Status

class IndexView(FailureMessageMixin, AuthRequireMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    fields = ['id', 'name', 'created_at']
    template_name = 'statuses/index.html'


class CreateStatusView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Status
    fields = ['name']
    template_name = 'statuses/create.html'
    success_message = _('Статус успешно создан')
    success_url = reverse_lazy('statuses:index')


class UpdateStatusView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Status
    fields = ['name']
    template_name = 'statuses/update.html'
    success_message = _('Статус успешно изменён')
    success_url = reverse_lazy('statuses:index')


class DeleteStatusView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_message = _('Статус успешно удалён')
    success_url = reverse_lazy('statuses:index')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(self.request, 'Статус используется, нельзя удалить')
            return redirect('statuses:index')
