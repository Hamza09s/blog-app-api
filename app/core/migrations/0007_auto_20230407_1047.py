# Generated by Django 3.2.18 on 2023-04-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_like_likes_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.AlterField(
            model_name='like',
            name='likes_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
