# Generated by Django 3.0.6 on 2020-07-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0011_auto_20200723_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
    ]
