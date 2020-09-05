# Generated by Django 3.0.6 on 2020-09-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0019_forum_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='forumimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='forum_images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
