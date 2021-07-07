from rest_framework import serializers
from .models import Discussion
from .models import Post
from .models import Reply
from .models import MemberLikeOrFlagPost
from .models import MemberLikeOrFlagReply


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class MemberLikeOrFlagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberLikeOrFlagPost
        fields = '__all__'

class MemberLikeOrFlagReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberLikeOrFlagReply
        fields = '__all__'