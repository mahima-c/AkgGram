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
        fields = ('first_name','last_name','id','username', 'email','password','confirm_password')

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
        model = get_user_model()
        fields = ('username', 'profile_image')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'posted_on')
        read_only_fields = ('author', 'id', 'posted_on')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)
    number_of_comments = serializers.SerializerMethodField()
    post_comments = serializers.SerializerMethodField(
        'paginated_post_comments')
    liked_by_req_user = serializers.SerializerMethodField()
# defaults to get_<field_name>
    class Meta:
        model = Post
        fields = ('id', 'author',  'photo',
                  'text', 'location', 'posted_on',
                  'number_of_likes', 'number_of_comments',
                  'post_comments', 'liked_by_req_user')

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    def paginated_post_comments(self, obj):
        page_size = 2
        paginator = Paginator(obj.post_comments.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        post_comments = paginator.page(page)
        serializer = CommentSerializer(post_comments, many=True)

        return serializer.data

    def get_liked_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

#Serializer for the user update

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password',
                  'fullname', 'bio', 'profile_image')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5},
                        'username': {'min_length': 3}}

    def update(self, instance, validated_data):
       # Update a user
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
