from django.contrib import messages
from django.shortcuts import redirect


class FailureMessageMixin():

    permission_denied_message = ''
    permission_denied_url = 'root'

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_url)
