# Generated by Django 2.2.4 on 2019-10-29 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_auto_20191028_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.RemoveField(
            model_name='user',
            name='no_post',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='website',
        ),
    ]
