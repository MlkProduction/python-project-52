from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Statuses(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.ForeignKey(
        Statuses, on_delete=models.PROTECT,
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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Labels(models.Model):
    name = models.CharField(max_length=300, verbose_name="Имя")
    tasks = models.ManyToManyField(Tasks, related_name='labels', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    

        