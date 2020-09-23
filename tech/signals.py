from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from notifications.signals import notify
from django.http import HttpResponse
from django.template import loader
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from .models import *

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
