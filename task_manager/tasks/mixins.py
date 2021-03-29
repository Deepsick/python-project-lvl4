from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class TaskAuthorRequireMixin(UserPassesTestMixin):
    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'Только автор может удалить свое задание')
        self.permission_denied_url = reverse_lazy('tasks:index')
        return super().dispatch(request, *args, **kwargs)
