'''This is a docstring'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event

admin.site.register(User, UserAdmin,)
admin.site.register(Event)
# Register your models here.
