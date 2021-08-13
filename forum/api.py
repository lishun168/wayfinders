from django.core.exceptions import PermissionDenied
from requests import Response
from rest_framework import viewsets, permissions
from members.models import MemberUser
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
from wayfinders.functions import add_to_queryset


class DiscussionAPI(viewsets.ModelViewSet):
    serializer_class = DiscussionSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        title = self.request.query_params.get('title')
        subtitle = self.request.query_params.get('subtitle')
        created_at = self.request.query_params.get('created_at')
        created_by_string = self.request.query_params.get('created_by_string')
        sticky = self.request.query_params.get('sticky')  # bool
        created_by_id = self.request.query_params.get('created_by_id')  # int
        likes = self.request.query_params.get('likes')  # int
        number_of_flags = self.request.query_params.get('number_of_flags')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'events_id__icontains', title)
        add_to_queryset(queryset_params, 'subtitle__icontains', subtitle)
        add_to_queryset(queryset_params, 'created_at__icontains', created_at)
        add_to_queryset(queryset_params, 'created_by_string__icontains', created_by_string)
        add_to_queryset(queryset_params, 'created_by_id', created_by_id)
        add_to_queryset(queryset_params, 'likes', likes)
        add_to_queryset(queryset_params, 'number_of_flags', number_of_flags)

        if (sticky == "true"):
            add_to_queryset(queryset_params, 'sticky', True)
        elif (sticky == "false"):
            add_to_queryset(queryset_params, 'sticky', False)

        if queryset_params:
            return Discussion.objects.filter(**queryset_params)
        return Discussion.objects.all()


class DiscussionPostAPI(viewsets.ModelViewSet):
    serializer_class = DiscussionSerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)
        # Discussion - no superuser or wf_admin check
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        # Discussion - no superuser or wf_admin check
        self.perform_update(serializer)
        return Response(serializer.data)


class PostAPI(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        body = self.request.query_params.get('body')
        created_by_string = self.request.query_params.get('created_by_string')
        created_at = self.request.query_params.get('created_at')
        edited_at = self.request.query_params.get('edited_at')
        edited = self.request.query_params.get('edited')  # bool
        likes = self.request.query_params.get('likes')  # int
        flagged = self.request.query_params.get('flagged')  # bool
        number_of_flags = self.request.query_params.get('number_of_flags')  # int
        created_by_id = self.request.query_params.get('created_by_id')  # int
        discussion_id = self.request.query_params.get('discussion_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'body__icontains', body)
        add_to_queryset(queryset_params, 'created_by_string__icontains', created_by_string)
        add_to_queryset(queryset_params, 'created_at__icontains', created_at)
        add_to_queryset(queryset_params, 'edited_at__icontains', edited_at)
        add_to_queryset(queryset_params, 'likes', likes)  # int
        add_to_queryset(queryset_params, 'number_of_flags', number_of_flags)  # int
        add_to_queryset(queryset_params, 'created_by_id', created_by_id)  # int
        add_to_queryset(queryset_params, 'discussion_id', discussion_id)  # int

        if (edited == "true"):
            add_to_queryset(queryset_params, 'edited', True)
        elif (edited == "false"):
            add_to_queryset(queryset_params, 'edited', False)

        if (flagged == "true"):
            add_to_queryset(queryset_params, 'flagged', True)
        elif (flagged == "false"):
            add_to_queryset(queryset_params, 'flagged', False)

        if queryset_params:
            return Post.objects.filter(**queryset_params)
        return Post.objects.all()


class PostPostAPI(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)
        # Post - no superuser or wf_admin check
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        # Post - no superuser or wf_admin check
        self.perform_update(serializer)
        return Response(serializer.data)


class ReplyAPI(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        body = self.request.query_params.get('body')
        created_by_string = self.request.query_params.get('created_by_string')
        created_at = self.request.query_params.get('created_at')
        edited_at = self.request.query_params.get('edited_at')
        edited = self.request.query_params.get('edited')  # bool
        likes = self.request.query_params.get('likes')  # int
        flagged = self.request.query_params.get('flagged')  # bool
        number_of_flags = self.request.query_params.get('number_of_flags')  # int
        created_by_id = self.request.query_params.get('created_by_id')  # int
        post_id = self.request.query_params.get('discussion_id')  # int
        discussion_id = self.request.query_params.get('discussion_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'body__icontains', body)
        add_to_queryset(queryset_params, 'created_by_string__icontains', created_by_string)
        add_to_queryset(queryset_params, 'created_at__icontains', created_at)
        add_to_queryset(queryset_params, 'edited_at__icontains', edited_at)
        add_to_queryset(queryset_params, 'likes', likes)
        add_to_queryset(queryset_params, 'number_of_flags', number_of_flags)
        add_to_queryset(queryset_params, 'created_by_id', created_by_id)
        add_to_queryset(queryset_params, 'post_id', post_id)
        add_to_queryset(queryset_params, 'discussion_id', discussion_id)

        if (edited == "true"):
            add_to_queryset(queryset_params, 'edited', True)
        elif (edited == "false"):
            add_to_queryset(queryset_params, 'edited', False)

        if (flagged == "true"):
            add_to_queryset(queryset_params, 'flagged', True)
        elif (flagged == "false"):
            add_to_queryset(queryset_params, 'flagged', False)

        if queryset_params:
            return Reply.objects.filter(**queryset_params)
        return Reply.objects.all()


class ReplyPostAPI(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        # Reply - no superuser or wf_admin check
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        # Reply - no superuser or wf_admin check
        self.perform_update(serializer)
        return Response(serializer.data)


class MemberLikeOrFlagPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagPostSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        flagged = self.request.query_params.get('flagged')  # bool
        like = self.request.query_params.get('like')  # bool
        member_id = self.request.query_params.get('member_id')  # int
        post_id = self.request.query_params.get('post_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'member_id', member_id)
        add_to_queryset(queryset_params, 'post_id', post_id)

        if (flagged == "true"):
            add_to_queryset(queryset_params, 'flagged', True)
        elif (flagged == "false"):
            add_to_queryset(queryset_params, 'flagged', False)

        if (like == "true"):
            add_to_queryset(queryset_params, 'like', True)
        elif (like == "false"):
            add_to_queryset(queryset_params, 'like', False)

        if queryset_params:
            return MemberLikeOrFlagPost.objects.filter(**queryset_params)
        return MemberLikeOrFlagPost.objects.all()

class MemberLikeOrFlagPostPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagPostSerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

class MemberLikeOrFlagReplyAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagReplySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        flagged = self.request.query_params.get('flagged')  # bool
        like = self.request.query_params.get('like')  # bool
        member_id = self.request.query_params.get('member_id')  # int
        reply_id = self.request.query_params.get('reply_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'member_id', member_id)
        add_to_queryset(queryset_params, 'reply_id', reply_id)

        if (flagged == "true"):
            add_to_queryset(queryset_params, 'flagged', True)
        elif (flagged == "false"):
            add_to_queryset(queryset_params, 'flagged', False)

        if (like == "true"):
            add_to_queryset(queryset_params, 'like', True)
        elif (like == "false"):
            add_to_queryset(queryset_params, 'like', False)

        if queryset_params:
            return MemberLikeOrFlagReply.objects.filter(**queryset_params)
        return MemberLikeOrFlagReply.objects.all()

class MemberLikeOrFlagReplyPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberLikeOrFlagReplySerializer
    http_method_names = ['post', 'put', 'patch']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()