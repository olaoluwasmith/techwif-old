# Generated by Django 3.0.6 on 2020-07-13 16:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tech', '0005_auto_20200712_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
