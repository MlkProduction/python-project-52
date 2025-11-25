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
        