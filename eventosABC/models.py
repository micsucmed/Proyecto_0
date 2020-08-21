'''This is a docstring'''
import datetime
import uuid
import requests
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from django.urls import reverse
# from django.utils.text import slugify
from rest_framework.authtoken.models import Token
from requests.auth import AuthBase

# Create your models here.
class User(AbstractUser):
    '''This is a docstring'''
    email = models.EmailField(unique=True)

# def uplaod_location(instance, filename):
#     '''This is a docstring'''
#     file_path = 'events_thumbnails/{event_id}.jpg'.format(event_id=str(instance.id))
#     return file_path

class Event(models.Model):
    '''This is a docstring'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_category = models.CharField(max_length=10, choices=[('CONFERENCE', 'CONFERENCE'),
                                                              ('SEMINAR', 'SEMINAR'),
                                                              ('CONGRESS', 'CONGRESS'),
                                                              ('COURSE', 'COURSE')])
    event_place = models.CharField(max_length=100)
    event_address = models.CharField(max_length=200)
    event_initial_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    event_final_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    event_type = models.CharField(max_length=10, choices=[('VIRTUAL', 'VIRTUAL'),
                                                          ('PRESENCIAL', 'PRESENCIAL')])
    # thumbnail = models.ImageField(upload_to=uplaod_location, default="static/Default_Thumbnail.png")

    def __str__(self):
        return self.event_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    '''This is a docstring'''
    if created:
        Token.objects.create(user=instance)

# @receiver(post_delete, sender=Event)
# def submission_delete(sender, instance, **kwargs):
#     '''This is a docstring'''
#     instance.thumbnail.delete(False)
