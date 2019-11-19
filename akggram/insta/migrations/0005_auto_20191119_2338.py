# Generated by Django 2.2.4 on 2019-11-19 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0004_post_tag_people'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag_people',
        ),
        migrations.AddField(
            model_name='post',
            name='tag_people',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tag', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]