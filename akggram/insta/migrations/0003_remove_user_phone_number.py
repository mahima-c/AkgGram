# Generated by Django 2.2.4 on 2019-10-25 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0002_auto_20191024_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
    ]
