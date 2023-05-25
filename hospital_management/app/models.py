from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pno = models.CharField(max_length=10)
    isDoctor = models.BooleanField(default=0)

