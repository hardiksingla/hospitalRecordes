from django.contrib import admin
from django.contrib.auth.models import User
from .models import pno, docinfo

admin.site.unregister(User)

class pnoinline(admin.StackedInline):
    model = pno

class docinfo(admin.StackedInline):
    model = docinfo

class UserAdmin(admin.ModelAdmin):
    model = User
    if pno.isDoctor == True:
        inlines = [pnoinline, docinfo]
    else:
        inlines = [pnoinline]
    fields = ['username', 'first_name', 'last_name', 'groups', 'user_permissions', 'email']

admin.site.register(User, UserAdmin)

admin.site.register(pno)