"""
Module to define user profile model
"""
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
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    After executing the user model, send the signal to create a profile
    """
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Method to save the registered user partial profile
    """
    instance.profile.save()
