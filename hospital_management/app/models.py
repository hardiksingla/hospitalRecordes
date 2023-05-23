from django.db import models

from django.contrib.auth.models import User

class pno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    number = models.BigIntegerField(blank=True)
    isDoctor = models.BooleanField(blank = False)

    def __str__(self):
        return self.user.username

class docinfo(models.Model):
    speciality = models.CharField(max_length=100)
    degree = models.CharField(max_length=20)
    apno = models.BigIntegerField(blank = True)

