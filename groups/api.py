from django.core.exceptions import PermissionDenied
from requests import Response
from rest_framework import viewsets, permissions
from members.models import MemberUser
from .models import Groups
from .models import Rules
from .models import GroupToMember
from .serializers import GroupsSerializer
from .serializers import RulesSerializer
from .serializers import GroupToMemberSerializer
from wayfinders.functions import add_to_queryset


class GroupsAPI(viewsets.ModelViewSet):
    serializer_class = GroupsSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        description = self.request.query_params.get('description')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'description__icontains', description)

        if queryset_params:
            return Groups.objects.filter(**queryset_params)
        return Groups.objects.all()

class GroupsPostAPI(viewsets.ModelViewSet):
    serializer_class = GroupsSerializer
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

class RulesAPI(viewsets.ModelViewSet):
    serializer_class = RulesSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        name = self.request.query_params.get('name')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)

        if queryset_params:
            return Rules.objects.filter(**queryset_params)
        return Rules.objects.all()

class RulesPostAPI(viewsets.ModelViewSet):
    serializer_class = RulesSerializer
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

class GroupToMemberAPI(viewsets.ModelViewSet):
    serializer_class = GroupToMemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id')  # int
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'group_id', group_id)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if queryset_params:
            return GroupToMember.objects.filter(**queryset_params)
        return GroupToMember.objects.all()

class GroupToMemberPostAPI(viewsets.ModelViewSet):
    serializer_class = GroupToMemberSerializer
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