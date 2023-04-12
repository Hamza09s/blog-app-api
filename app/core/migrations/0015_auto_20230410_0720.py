# Generated by Django 3.2.18 on 2023-04-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20230410_0709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='blog',
        ),
        migrations.RemoveField(
            model_name='like',
            name='like',
        ),
        migrations.AddField(
            model_name='like',
            name='likes_count',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(default=None, null=True, related_name='likes', to='core.Like'),
        ),
    ]
