from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from notifications.signals import notify
from django.http import HttpResponse
from django.template import loader
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

"""
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, **kwargs):

    subject = 'Welcome to Techwif'
    from_email = 'no-reply@techwif.com'
    to = instance.email
    plaintext = loader.get_template('user/welcome.txt')
    html = loader.get_template('user/welcome.html')

    d = {'username': instance.username}

    text_content = plaintext.render(d)
    html_content = html.render(d)

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
"""