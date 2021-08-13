from django.core.exceptions import PermissionDenied
from django.db.models import query
from requests import Response
from rest_framework import viewsets, permissions

from members.models import MemberUser
from .serializers import SkillSerializer, UserToSkillsSerializer, MemberToSkillsSerializer
from .models import Skill, MemberToSkills, UserToSkills
from wayfinders.functions import add_to_queryset

import logging

logger = logging.getLogger('skills.api')


class SkillAPI(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        description = self.request.query_params.get('description')
        official = self.request.query_params.get('official')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'description__icontains', description)

        # Strings icontains, Booleans if statement, Integer equals

        if (official == "true"):
            add_to_queryset(queryset_params, 'official', True)
        elif (official == "false"):
            add_to_queryset(queryset_params, 'official', False)

        if queryset_params:
            return Skill.objects.filter(**queryset_params)

        return Skill.objects.all()


class SkillPostAPI(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
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


class MemberToSkillsAPI(viewsets.ModelViewSet):
    serializer_class = MemberToSkillsSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        member_id = self.request.query_params.get('member_id')  # int
        skill_id = self.request.query_params.get('skill_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'member_id', member_id)
        add_to_queryset(queryset_params, 'skill_id', skill_id)

        if queryset_params:
            return MemberToSkills.objects.filter(**queryset_params)

        return MemberToSkills.objects.all()


class MemberToSkillsPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberToSkillsSerializer
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


class UserToSkillsAPI(viewsets.ModelViewSet):
    serializer_class = UserToSkillsSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')  # int
        skill_id = self.request.query_params.get('skill_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'user_id', user_id)
        add_to_queryset(queryset_params, 'skill_id', skill_id)

        if queryset_params:
            return UserToSkills.objects.filter(**queryset_params)

        return UserToSkills.objects.all()


class UserToSkillsPostAPI(viewsets.ModelViewSet):
    serializer_class = UserToSkillsSerializer
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
