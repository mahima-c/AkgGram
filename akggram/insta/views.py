from .serializers import *
from .permissions import *
from django.db.models import Q
from .backends import EmailOrUsername
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status,filters
from rest_framework import generics,viewsets,mixins
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from akggram.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class SignUp(APIView):
    """
    List all user, or create a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver=user)
        data.save()
        user.is_active = False
        user.save()
        subject = 'Activate Your  Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
         })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': username+',Please confirm your email to complete registration.',
                                'user_id': user.id })


class Activate(APIView):
    """
    Activate verifies the stored otp and the otp entered by user.
    """
    permission_classes = (permissions.AllowAny,IsNotActive)
    serializer_class = OTPSerializer

    def post(self,request,user_id,*args,**kwargs):
        code = OTPSerializer(data=request.data)
        code.is_valid(raise_exception=True)
        code = code.validated_data['otp']
        try:
            otp = OTP.objects.get(receiver=user_id)
        except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
                otp = None
        try:
            receiver = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            receiver = None
        if otp is None or receiver is None:
            return Response({'error':'you are not a valid user'},status=status.HTTP_400_BAD_REQUEST)

        elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
            otp.delete()
            return Response({'detail':'OTP expired!',
                                 'user_id':user_id})

        if otp.otp == code:
            receiver.is_active = True
            receiver.save()
            user = User.objects.get(role='user')
            receiver.roles.add(user)
            otp.delete()
            return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class ResendOtp(generics.CreateAPIView):
    """
    views for resend the otp.
    """
    serializer_class = OTPSerializer
    permission_classes = (permissions.AllowAny,IsNotActive)

    def get(self,request,user_id,*args,**kwargs):
        try:
            user = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response({'error':'Not a valid user!'})
        otp = OTP.objects.filter(receiver=user)
        if otp:
            otp.delete()
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver= user)
        data.save()
        subject = 'Activate Your Dealmart Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': user.username +',Please confirm your email to complete registration.',
                         'user_id': user_id },
                        status=status.HTTP_201_CREATED)

class Login(APIView):
    """
    the user can login either with email or username. EmailOrUsername is the function for it.
    """

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uname_or_em = serializer.validated_data['uname_or_em']
        password = serializer.validated_data['password']
        user = EmailOrUsername(self,uname_or_em = uname_or_em,password=password)

        if user == 2:
            return Response({'error':'Invalid Username or Email!!'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        elif user == 3:
            return Response({'error':'Incorrect Password'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            if user.is_active:
                login(request, user)
                return Response({'detail':'successfully Logged in!','user_id': user.id,
                                 'username':user.username},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error':'Please! varify Your Email First','user_id':user.id},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)


class Logout(APIView):
    
    def get(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'successfully logged out'},
                        status=status.HTTP_200_OK)
