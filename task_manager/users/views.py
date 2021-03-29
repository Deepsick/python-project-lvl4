from django.contrib.auth import get_user_model, views as auth_views
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import UserForm
from .mixins import AuthRequireMixin, UserTestAccountMixin
from task_manager.mixins import FailureMessageMixin


class IndexView(ListView):
    model = get_user_model()
    context_object_name = 'users'
    template_name = 'users/index.html'
    fields = ['id', 'username', 'first_name',
              'last_name', 'date_joined']


class CreateUserView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = 'users/create.html'
    form_class = UserForm
    success_message = _("Регистрация прошла успешна")
    success_url = reverse_lazy('users:login')


class LoginUserView(SuccessMessageMixin, auth_views.LoginView):
    template_name = 'users/login.html'
    success_message = _('Вы залогинены')


class LogoutUserView(SuccessMessageMixin, auth_views.LogoutView):
    success_message = _('Вы разлогинены')


class UpdateUserView(
    FailureMessageMixin,
    AuthRequireMixin,
    UserTestAccountMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/update.html'
    success_message = _('Пользователь успешно обновлен')


class DeleteUserView(
    FailureMessageMixin,
    AuthRequireMixin,
    UserTestAccountMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('Пользователь успешно удален')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(
                self.request, 'Пользователь - автор заданий, нельзя удалить')
            return redirect('users:index')
