# Generated by Django 2.2.4 on 2019-11-08 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0002_auto_20191108_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, editable=False, upload_to=''),
        ),
    ]