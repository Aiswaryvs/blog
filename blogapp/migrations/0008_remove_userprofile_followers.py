# Generated by Django 4.0.4 on 2022-07-19 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_userprofile_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followers',
        ),
    ]
