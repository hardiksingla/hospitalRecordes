from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class types(models.TextChoices):
        doctor = "doctor"
        hospital = "hospital"

    type = models.CharField(choices=types.choices, max_length=9, default=types.hospital)
    pno = models.CharField(max_length=10)

class hospitalMore(models.Model):
    hospital = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.TextField(null=True)
    regID = models.CharField(max_length=100)
    altpno = models.CharField(max_length=10, null=True)

class doctorsMore(models.Model):
    doctor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name="doctor_key")
    hospital = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name="hospital_key") 
    altpno = models.CharField(max_length=10, null=True)
    speciality = models.CharField(max_length=70, null = True)
    degree = models.CharField(max_length=20, null = True)
    gender = models.CharField(max_length=6, null = True)
    dob = models.CharField(max_length=10, null = True)

    def __str__(self):
        return self.doctor.username
    
class patient(models.Model):

    genders = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender", "Transgender")
    )

    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(choices = genders, max_length=12, null="Male")
    pno = models.CharField(max_length=10)
    email = models.EmailField()
    diagnosis = models.TextField()
    prescription = models.TextField()
    last_visit = models.DateField(default = date.today)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.fname} {self.lname}"