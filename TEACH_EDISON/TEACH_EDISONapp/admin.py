# accounts.admin.py

from django.contrib import admin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
admin.site.register(User)