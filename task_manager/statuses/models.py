from django.db import models


class Status(models.Model):
    name = models.CharField('name', max_length=50, unique=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)

    def __str__(self):
        return self.name
