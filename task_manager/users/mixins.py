from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _


class AuthRequireMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _('Вы не авторизованы')
        self.permission_denied_url = reverse_lazy('login')
        return super().dispatch(request, *args, **kwargs)


class UserTestAccountMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'Вы не можете редактировать чужик аккаунты')
        self.permission_denied_url = reverse_lazy('users:index')
        return super().dispatch(request, *args, **kwargs)
