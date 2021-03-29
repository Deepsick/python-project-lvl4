from django.db import models
from django.utils.translation import gettext_lazy as _

class Status(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def __str__(self):
        return self.name
