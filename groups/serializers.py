from rest_framework import serializers
from .models import Groups
from .models import Rules
from .models import GroupToMember


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = '__all__'


class GroupToMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupToMember
        fields = '__all__'