# Generated by Django 4.0.6 on 2022-07-21 12:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_remove_reply_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
