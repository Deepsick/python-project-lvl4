from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label


User = get_user_model()


class Task(models.Model):
    name = models.CharField('name', max_length=200)
    description = models.TextField('description')
    author = models.ForeignKey(
        User, related_name='author', verbose_name='author', blank=True,
        null=True,
        on_delete=models.PROTECT)
    status = models.ForeignKey(
        Status,
        related_name='status',
        verbose_name="status",
        on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User,
        related_name='executor',
        verbose_name='user',
        on_delete=models.PROTECT
    )
    labels = models.ManyToManyField(
        Label,
        related_name='labels',
        through='TaskLabel',
        verbose_name='labels'
    )
    created_at = models.DateTimeField('created_at', auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, related_name='task',
                             verbose_name='task', on_delete=models.CASCADE)
    label = models.ForeignKey(
        Label,
        related_name='label',
        verbose_name='label',
        on_delete=models.PROTECT
    )
