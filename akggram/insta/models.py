from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

# Create your models here.



'''class Role(models.Model):
    """
    this is defined to allot a role to a user.
    """
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20,unique=True,default="user")

    def __str__(self):
        return '%s'%(self.role)
'''

class User(AbstractUser):
    """
    user is customised and related to model Role using Abstract user.
    """
    username=models.CharField(max_length=200,unique=True)
    email=models.EmailField(max_length=200,unique=True,help_text='Required')
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)



class OTP(models.Model):
    """
    Model to store Otp of user And verify user.
    """
    receiver = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.IntegerField(null=False,blank=False)
    sent_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("%s has received otps: %s" %(self.receiver.username,self.otp))
