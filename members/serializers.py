from rest_framework import serializers
from .models import Member
from .models import MemberUser
from .models import UserToMember
from .models import Permissions
from .models import UserRole
from .models import Gallery
from .models import Application


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class MemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = '__all__'


class UserToMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToMember
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
