from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(OTP)
admin.site.register(User)

