# Generated by Django 3.2.18 on 2023-04-11 07:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_blog_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(related_name='Like', to=settings.AUTH_USER_MODEL),
        ),
    ]
