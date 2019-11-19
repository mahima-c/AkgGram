from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
import json
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    """
    serializer for creating user object
    """
    email = serializers.EmailField(required=True,allow_blank=False,allow_null=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="email already exists!",
                                                               lookup='exact')])
    username = serializers.CharField(required=True,allow_blank=False,allow_null=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="username is taken!,try another",
                                                                 lookup='exact')])
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)
    confirm_password = serializers.CharField(style={'input_type':'password'},required=True)

    class Meta:
        model = User
        fields = ('fullname','id','username', 'email','password','confirm_password')

    def validate(self, data):


        password = data.get('password')
        pass_cnf = data.get('confirm_password')

        if password != pass_cnf:
               raise ValidationError("Password didn't matched ")
        if len(password) < 6:
               raise ValidationError("password of minimum 6 digit is required")
        else:
            return data

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','id')

class OTPSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = OTP
        fields = ['otp']
# class StorySerializer(serializers.ModelSerializer):
    

#     class Meta:
#         model = Story
#         fields = ['photo']

'''class LoginSerializer(serializers.ModelSerializer):
    

    uname_or_em = serializers.CharField(allow_null=False,required=True)
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)

    class Meta:
        model = User
        fields = ('uname_or_em','password')

'''
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'profile_image')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'posted_on')
        read_only_fields = ('author', 'id', 'posted_on')

class StorySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)


    class Meta:
        model = Story
        fields = ['photo','id', 'author']

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)
    number_of_comments = serializers.SerializerMethodField()
    post_comments = serializers.SerializerMethodField(
        'all_post_comments')
# defaults to get_<field_name>
    class Meta:
        model = Post
        fields = ('id', 'author',  'photo',
                  'text', 'location', 'posted_on',
                  'number_of_likes', 'number_of_comments',
                  'post_comments')

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()
    #for showing user comment

    def all_post_comments(self, obj):
        # page_size = 2 #only last two comment are view
        # paginator = Paginator(obj.post_comments.all(), page_size)
        # page = self.context['request'].query_params.get('page') or 1

        post_comments = obj.post_comments.all()
        serializer = CommentSerializer(post_comments, many=True)

        return serializer.data

   
class Userfeed(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)
    class Meta:
        model = Post
        fields = '__all__'

#Serializer for the user update

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (      'id',
                        'email', 
                        'username', 
                        'password',
                        'fullname', 
                        'bio', 
                        'profile_image')
        extra_kwargs = {'password': {'write_only': True} }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class UserPostsSerializer(serializers.ModelSerializer):
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 
                    'photo', 
                    'text', 
                    'location', 
                    'number_of_likes',
                  'number_of_comments', 
                  'posted_on')

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count() 
        
               
class UserProfileSerializer(serializers.ModelSerializer):
    number_of_posts = serializers.SerializerMethodField()
    user_posts = serializers.SerializerMethodField('all_user_posts')

    class Meta:
        model = User
        fields = ('id', 
                    'username', 
                    'fullname',
                    'bio', 
                    'profile_image', 
                    'number_of_followers',
                    'number_of_following', 
                    'number_of_posts',
                     'user_posts')
    #for finding no of post
    def get_number_of_posts(self, obj):
        return Post.objects.filter(author=obj).count()
        
    #for showing user post
    def all_user_posts(self, obj):
     
        user_posts = obj.user_posts.all()
        serializer = UserPostsSerializer(user_posts, many=True)

        return serializer.data


class FollowSerializer(serializers.ModelSerializer):
#Serializer for listing all followers

    class Meta:
        model = User
        fields = ('username', 'profile_image')

class NotificationSerializer(serializers.ModelSerializer):

    creator = AuthorSerializer()
    image = PostSerializer()

    class Meta:
        model = Notification
        fields = '__all__'        