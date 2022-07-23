# Generated by Django 4.0.6 on 2022-07-21 12:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 7, 21, 12, 38, 20, 770794, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reply',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 7, 21, 12, 38, 28, 771460, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reply',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='commentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_posts', to='Blog.post'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Blog.comments'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='commentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repliers', to=settings.AUTH_USER_MODEL),
        ),
    ]
