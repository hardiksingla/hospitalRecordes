from django.contrib import admin
from django.contrib.auth.models import User
from .models import CustomUser

admin.display
admin.site.register(CustomUser)