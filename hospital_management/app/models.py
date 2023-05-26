from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class types(models.TextChoices):
        doctor = "doctor"
        hospital = "hospital"

    type = models.CharField(choices=types.choices, max_length=9, default=types.hospital)
    pno = models.CharField(max_length=10)


class doctorsMore(models.Model):
    doctor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    altpno = models.CharField(max_length=10, null=True)
    speciality = models.CharField(max_length=70, null = True)
    degree = models.CharField(max_length=20, null = True)
    gender = models.CharField(max_length=6, null = True)
    dob = models.CharField(max_length=10, null = True)

    def __str__(self):
        return self.doctor.username

class hospitalMore(models.Model):
    hospital = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    regID = models.CharField(max_length=100)

class doctorsManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filer(type = CustomUser.types.doctor)


class hospitalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filer(type = CustomUser.types.hospital)

class doctors(CustomUser):
    base_type = CustomUser.types.doctor
    objects = doctorsManager()

    @property
    def more(self):
        return self.doctorMore

    class Meta:
        proxy = True

class hospitals(CustomUser):
    objects = hospitalManager()

    @property
    def more(self):
        return self.hospitalMore

    class Meta:
        proxy = True