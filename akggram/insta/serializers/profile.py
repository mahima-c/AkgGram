from rest_framework.serializers import ModelSerializer,PrimaryKeyRelatedField, SerializerMethodField
from insta.models import Profile


class ProfileSerializer(ModelSerializer):
    
    class Meta:
        module = Profile
        fields = (
            'id',
            'website_url',
        )

        read_only_fields = ('id',)
