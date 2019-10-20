from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from insta.serializers.profile import ProfileSerializer
from insta.serializers.user import UserSerializer
from insta.auth.utils import AuthTools
from rest_framework.authtoken.models import Token

User = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'email',
            'first_name',
            'last_name',
            'password',
        )
        write_only_fields = (
            'email',
            'first_name',
            'last_name',
            'password',
        )
        def save(self, **kwargs):
            data = self.init_data if hasattr(self,'init_data') else self.initial_data

            items = dict(data.items())
            user_data = {
                'username':items['username'],
                'email': items['email'],
                'password': items['password'],

            }
            profile_data = {
                'role':'consumer',
            }
            group = profile_data['role']+'_basic'
            user = AuthTools.register(user_data,profile_data,group)
            if user is not None:
                self.object = user
                return self.object

            raise serializers.ValidationError('unable to register with the credential provied')

class LoginSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    user = UserSerializer(many=False)
    class Meta:
        model = Token
        fields = (
            'auth_token',
            'user'
        )
        read_only_fields = fields



