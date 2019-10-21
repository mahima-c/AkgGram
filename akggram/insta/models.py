from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES =(
        ('consumer','Consumer'),
        ('staff','Staff')

    )
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    bio = models.TextField(blank=True,null=True)
    website_url = models.CharField(blank=True,null=True,max_length=100)
    role = models.CharField(max_length=8,choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username




