from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField, SerializerMethodField
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    
    #class Meta:
        module = User
        fields = (
            'id',
            'username',
            'email',
        )

        read_only_fields = ('id',)
