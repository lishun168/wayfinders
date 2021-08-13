from rest_framework import serializers
from .models import Skill, MemberToSkills, UserToSkills


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class MemberToSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberToSkills
        fields = '__all__'

class UserToSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToSkills
        fields = '__all__'
