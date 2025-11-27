from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    username = models.CharField(max_length=300)
    fullname = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class Statuses(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    name = models.CharField(max_length=300)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, related_name='tasks')
    author = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='authored_tasks', null=True, blank=True) #id?
    executor = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='executed_tasks', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Labels(models.Model):
    name = models.CharField(max_length=300)
    tasks = models.ManyToManyField(Tasks, related_name='labels', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    

        