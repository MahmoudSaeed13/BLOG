# Generated by Django 4.0.6 on 2022-07-22 17:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0012_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likes',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
