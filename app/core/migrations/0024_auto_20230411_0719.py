# Generated by Django 3.2.18 on 2023-04-11 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20230411_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='blog',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.blog'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
