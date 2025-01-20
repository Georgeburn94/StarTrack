# Generated by Django 4.2.18 on 2025-01-20 10:38

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image'),
        ),
    ]
