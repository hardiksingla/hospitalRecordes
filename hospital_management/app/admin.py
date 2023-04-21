from django.contrib import admin
from django.contrib.auth.models import User
from .models import pno

admin.site.unregister(User)

class pnoinline(admin.StackedInline):
    model = pno

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [pnoinline]
    fields = ['username', 'first_name', 'last_name', 'groups', 'user_permissions', 'email']

admin.site.register(User, UserAdmin)

admin.site.register(pno)