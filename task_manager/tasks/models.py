from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT,
        related_name='tasks', verbose_name="Статус"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='authored_tasks', null=True, blank=True,
        verbose_name="Автор"
    )
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='executed_tasks', null=True, blank=True,
        verbose_name="Исполнитель"
    )
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
