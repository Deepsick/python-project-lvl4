from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class Task(models.Model):
    name = models.CharField(verbose_name=_('Имя'), max_length=200, unique=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True,)
    author = models.ForeignKey(
        User, related_name='author', verbose_name=_('Автор'), blank=True,
        null=True,
        on_delete=models.PROTECT)
    status = models.ForeignKey(
        Status,
        related_name='status',
        verbose_name=_('Статус'),
        on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User,
        related_name='executor',
        verbose_name=_('Исполнитель'),
        on_delete=models.PROTECT
    )
    labels = models.ManyToManyField(
        Label,
        related_name='labels',
        through='TaskLabel',
        verbose_name=_('Метки'),
        blank=True,
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, related_name='task',
                             verbose_name='task', on_delete=models.CASCADE)
    label = models.ForeignKey(
        Label,
        related_name='label',
        verbose_name=_('label'),
        on_delete=models.PROTECT
    )
