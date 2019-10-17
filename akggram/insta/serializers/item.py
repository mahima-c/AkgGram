from rest_framework import ModelSerializer,PrimaryKeyRelatedField, SerializerMethodField
from insta.models import Item
from django.contrib.auth.models import User
from insta.serializers.user import UserSerializer


class ItemSerializer(ModelSerializer):
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'subtitle',
            'owner',

        )
        read_only_fields = ('id',)


class ItemDetailSerializer(ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    fields = (
        'id',
        'title'
        'subtitle',
        'create_at',
        'updated_at',
    )



