# Generated by Django 4.0.6 on 2022-07-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0010_categorysubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='user/images/', verbose_name='User image'),
        ),
    ]
