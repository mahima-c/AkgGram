# Generated by Django 2.2.4 on 2019-10-29 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0009_comment_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='no_post',
        ),
    ]