from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts

# Register your models here.
admin.site.register(Accounts, UserAdmin)
