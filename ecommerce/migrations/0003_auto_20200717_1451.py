# Generated by Django 3.0.6 on 2020-07-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='products/'),
        ),
    ]
