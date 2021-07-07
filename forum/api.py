from rest_framework import viewsets
from .models import Discussion
from .models import Post
from .models import Reply
from .models import MemberLikeOrFlagPost
from .models import MemberLikeOrFlagReply
from .serializers import DiscussionSerializer
from .serializers import PostSerializer
from .serializers import ReplySerializer
from .serializers import MemberLikeOrFlagPostSerializer
from .serializers import MemberLikeOrFlagReplySerializer


class DiscussionAPI(viewsets.ModelViewSet):
    serializer_class = DiscussionSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Discussion.objects.all()

class PostAPI(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Post.objects.all()

class ReplyAPI(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Reply.objects.all()

class MemberLikeOrFlagPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagPostSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = MemberLikeOrFlagPost.objects.all()

class MemberLikeOrFlagReplyAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagReplySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = MemberLikeOrFlagReply.objects.all()