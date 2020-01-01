# from django.shortcuts import render

# def index(request):
#     return render(request, 'insta/index.html', {})

# from django.utils.safestring import mark_safe
# import json


# def room(request, room_name):
#     return render(request, 'insta/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name))
#     })









#...............................................api............................#
         
from .serializers import *
from .permissions import *
from django.db.models import Q
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
from rest_framework.authtoken.models import Token

 
from rest_framework import permissions, \
    viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, AuthorSerializer
from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly, IsOwnerOrPostOwnerOrReadOnly

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
        fullname = serializer.validated_data['fullname']
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username,email=email,password=password,fullname=fullname)
        otp = randint(10000, 100000)
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

        elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=5,seconds=0):
            otp.delete()
            return Response({'detail':'OTP expired!',
                                 'user_id':user_id})

        if otp.otp == code:
            receiver.is_active = True
            receiver.save()
            otp.delete()

            return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class ResendOtp(generics.CreateAPIView):
   
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
        subject = 'Activate Your  Account'
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

# class Storyviewset(viewsets.ModelViewSet):
#     serializer_class = StorySerializer
#     queryset = Story.objects.all()
#     permission_classes = (
#         IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
class Storyviewset(APIView):
    serializer_class = StorySerializer

    def post(self,request,*args,**kwargs):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        try:
            user= self.request.user
            story = Story.objects.get(author=user)
            print(story,"hi")
        except(TypeError, ValueError, OverflowError, Story.DoesNotExist):
            pass
            story = None
        if story:
            if timezone.now() - story.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
                story.delete()
                # storyy=Story.objects.get(author=self.user)
                return Response({'detail':'story deleted!'})
                # serializer = StorySerializer(story, many=True)#

                # return Response(serializer.data)#
        # save = Story.objects.filter(author=user)       
        return Response({'info':story})#
        # serializer = StorySerializer(story, many=True)
        # return Response(serializer.data)
# class StoryViewSet(viewsets.ViewSet):
#     serializer_class = StorySerializer
#     permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)    


#     def list(self, request):
#         try:
#             story = Story.objects.get(author=self.user)
#         except(TypeError, ValueError, OverflowError, story.DoesNotExist):
#             story = None
#         if timezone.now() - story.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
#             story.delete()
#             serializer = StorySerializer(story, many=True)

#             return Response(serializer.data)

#     def create(self, request):    
#         serializer = StorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        



# This viewset automatically provides `list` and `detail` actions.`retrieve``update` and `destroy` actions.

#post view
class Postviewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (
        IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# comment added views
class Addcommentview(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # queryset = Story.objects.all()
    def post(self, request, post_id=None):
        post = Post.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#for manage the commment
class Managecommentview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsOwnerOrPostOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset

#like view
class Likeview(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


class Likeviewown(APIView):

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = True
            else:
                like = False
        data = {
            'like': like
        }
        return Response(data)        
class Getlikers(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.get(pk=post_id).likes.all()
        return queryset

# list of post ,user-following
# done 
class Userfeed(generics.ListAPIView):
    serializer_class =  PostSerializer
    permission_classes = (
         IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    def get_queryset(self):

        user = self.request.user
        post = Post.objects.filter(author__in=user.following.all())
        return post


 
#edit the profile
#done
class Updateuserview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditProfileSerializer

    def get_object(self):
        return self.request.user
        
#for see the profile
class Userprofileview(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset =  User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)

#edit the profile
#done
class Updateuserview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditProfileSerializer

    def get_object(self):
        return self.request.user
    
#for save the post    
class Postsaveview(APIView):
    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if post in user.save_post.all():
                Save = False
                user.save_post.remove(post)
            else:
                Save = True
                user.save_post.add(post)
        data = {
            'Save': Save
        }
        return Response(data)

#for viewing the save post
#done
class Getsavepost(generics.ListAPIView):
    serializer_class =  PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        user = self.request.user
        post = user.save_post.all()
        return post

# class Getsavepost(generics.ListAPIView):
#     serializer_class = PostSerializer
#     # permission_classes = (permissions.AllowAny,)

#     def get_object(self):
#         user = self.request.user
#         queryset = user.objects.get().save_post.all()

#         return queryset        

#function for following  
# done 
class Followuserview(APIView):
    def get(self, request, format=None, username=None):
        username = self.kwargs['username']
        #u=User.objects.get(username=username)
        try:
            #if u:
            if User.objects.get(username=username):
                follow_user=User.objects.get(username=username)# follow user
                login_user=self.request.user #login user
                follow = None
                if login_user.is_authenticated:
                    if login_user != follow_user:
                        if login_user in follow_user.followers.all():
                            follow = False
                            login_user.following.remove(follow_user)
                            follow_user.followers.remove(login_user)
                        else:
                            follow = True
                            login_user.following.add(follow_user)
                            follow_user.followers.add(login_user)
                data = {
                    'follow': follow
                }
                return Response(data)
        except(User.DoesNotExist,IndexError,ValueError):
            return Response({"error": "not found"},status=status.HTTP_400_BAD_REQUEST)
          
#for listing the follower view
#done
class Getfollowersview(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs['username']
        queryset =  User.objects.get(
            username=username).followers.all()
        return queryset

#following
#done
class Getfollowingview(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = User.objects.get(
            username=username).following.all()
        return queryset        

#for searching by username
class Searchviewset(generics.ListAPIView):
    # serializer_class = UserProfileSerializer
    # queryset = User.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['username']
    serializer_class = UserProfileSerializer

    def get(self,username):
        username = self.kwargs['username']
        # try:
        queryset= User.objects.filter(username=username)
        return queryset
        # except(User.DoesNotExist,IndexError,ValueError):
        #     return Response({"error": "user not found"},status=status.HTTP_400_BAD_REQUEST)
# class Userfeed(generics.ListAPIView):
#     serializer_class =  PostSerializer
#     queryset = Post.objects.all()
#     permission_classes = (
#         IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
#     def get(self,username):
#         username = self.kwargs['username']
#         Post= Post.author.objects.(username=username)







# class Notifcation(APIView):
#     serializer_class =  NotificationSerializer
#     queryset =  Notification.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    
#     def get(self, request, format=None):
#         user = request.user
#         notifications = models.Notification.objects.filter(to=user)
#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data)
#     def perform_create():
#         notification = Notification.objects.create()   

