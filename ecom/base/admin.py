from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister and register the User model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

