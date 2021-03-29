from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import views
from django.utils.translation import gettext_lazy as _

class IndexView(TemplateView):
    template_name = 'task_manager/index.html'


class LoginView(SuccessMessageMixin, views.LoginView):
    template_name = 'users/login.html'
    success_message = _('Вы залогинены')


class LogoutView(SuccessMessageMixin, views.LogoutView):
    success_message = _('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
