from rest_framework import serializers
from .models import SearchObject
from .models import SearchTags


class SearchObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchObject
        fields = '__all__'


class SearchTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTags
        fields = '__all__'
