from django.contrib.auth import get_user_model
from django.conf import settings 
from rest_framework import generics,status
from rest_framework.response import Response
from insta.auth import AuthTools
from insta import settings as api_settings
from insta.auth import serializers
from insta.serializers import profileSerializer
from insta.serializers import UserSerializer
from insta.models import Profile
import re


User = get_user_model()
class UserView(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    Permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get_object(self,*args,**kwargs):
        return self.request.user

class ProfileView(generics.RetrieveAPIView):
    model = User.profile
    serializer_class = profileSerializer
    Permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get_object(self,*args,**kwargs):
        return self.request.user.profile


class Loginview(generics.RetrieveAPIView):
    Permission_classes = api_settings.UNPROTECTED
    def post(self,request):
        if 'email' in request.data and 'password' in request.data:

            email = request.data['email'].lower()
            password = request.data['password']

            user = AuthTools.authenticate_email(email,password)

            if user is not None and AuthTools.login(request,user):
                token = AuthTools.issue_user_token(user,'login')
                serializers = serializers.LoginSerializer(token)
                return Response(serializers.data)

        message ={'message':'unable to login with the credentials provided'} 
        return Response(message,status=status.HTTP_400_BAD_REQUEST)    

        
class LogoutView(generics.RetrieveAPIView):
    Permission_classes = api_settings.CONSUMER_PERMISSIONS
    def post(self,request):
        if AuthTools.logout(request):
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.RetrieveAPIView):
    serializer_class = serializers.UserRegisterSerializer
    Permission_class = api_settings.UNPROTECTED

    def perform_create(self,serializer):
        isinstance = serializer.save()






