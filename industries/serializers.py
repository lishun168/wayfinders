from rest_framework import serializers
from .models import Industry
from .models import MemberToIndustry
from .models import UsertoIndustry

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class MemberToIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberToIndustry
        fields = '__all__'

class UsertoIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsertoIndustry
        fields = '__all__'