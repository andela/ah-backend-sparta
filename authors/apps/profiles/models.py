"""
Module to define user profile model
"""
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.authentication.models import User



class Profile(models.Model):
    """
    Class to handle creation of user profiles
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


def save_profile(sender, instance, **kwargs):
    Profile.objects.create(user=instance, username=instance.username)
    instance.profile.save()
post_save.connect(save_profile, sender=User)


    
