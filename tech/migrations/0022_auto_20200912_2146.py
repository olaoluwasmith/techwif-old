# Generated by Django 3.0.6 on 2020-09-12 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0021_auto_20200907_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, max_length=500, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='forumimages',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='forum_images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', max_length=500, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, max_length=500, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, max_length=500, upload_to='images/'),
        ),
    ]