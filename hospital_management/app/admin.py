from typing import Optional, Type
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from .models import CustomUser, doctorsMore

admin.display
admin.site.register(doctorsMore)

class doctorsMoreinline(admin.StackedInline):
    model = doctorsMore

    def __str__(self):
        return self.doctor.username

class user(admin.ModelAdmin):
    inlines = [doctorsMoreinline]

admin.site.register(CustomUser, user)