# Generated by Django 2.0.7 on 2018-08-05 22:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suburban_dictionary', '0006_auto_20180805_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='disliked_by',
            field=models.ManyToManyField(blank=True, related_name='disliked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='definition',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]