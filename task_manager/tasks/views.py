from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from task_manager.users.mixins import AuthRequireMixin
from .mixins import TaskAuthorRequireMixin
from task_manager.mixins import FailureMessageMixin
from .models import Task
from .filter import TaskFilter


class IndexView(FailureMessageMixin, AuthRequireMixin, FilterView):
    model = Task
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    fields = ['id', 'name', 'status', 'author', 'executor', 'created_at']
    template_name = 'tasks/index.html'


class CreateTaskView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    CreateView
):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/create.html'
    success_message = _('Задача успешно создана')
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(
    FailureMessageMixin,
    AuthRequireMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/update.html'
    success_message = _('Задача успешно изменена')
    success_url = reverse_lazy('tasks:index')


class DeleteTaskView(
    FailureMessageMixin,
    AuthRequireMixin,
    TaskAuthorRequireMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Task
    template_name = 'tasks/delete.html'
    success_message = _('Задача успешно удалена')
    success_url = reverse_lazy('tasks:index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTaskView, self).delete(request, *args, **kwargs)


class DetailTaskView(FailureMessageMixin, AuthRequireMixin, DetailView):
    model = Task
    context_object_name = 'task'
    fields = ['id', 'name', 'status', 'author',
              'executor', 'labels', 'created_at']
    template_name = 'tasks/detail.html'
