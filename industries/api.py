from django.core.exceptions import PermissionDenied
from requests import Response
from rest_framework import viewsets, permissions

from members.models import MemberUser
from .models import Industry
from .models import MemberToIndustry
from .models import UsertoIndustry
from .serializers import IndustrySerializer
from .serializers import MemberToIndustrySerializer
from .serializers import UsertoIndustrySerializer
from wayfinders.functions import add_to_queryset


class IndustryAPI(viewsets.ModelViewSet):
    serializer_class = IndustrySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        description = self.request.query_params.get('description')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'description__icontains', description)

        if queryset_params:
            return Industry.objects.filter(**queryset_params)
        return Industry.objects.all()


class IndustryPostAPI(viewsets.ModelViewSet):
    serializer_class = IndustrySerializer
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


class MemberToIndustryAPI(viewsets.ModelViewSet):
    serializer_class = MemberToIndustrySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry_id')  # int
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'industry_id', industry_id)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if queryset_params:
            return MemberToIndustry.objects.filter(**queryset_params)
        return MemberToIndustry.objects.all()


class MemberToIndustryPostAPI(viewsets.ModelViewSet):
    serializer_class = MemberToIndustrySerializer
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


class UsertoIndustryAPI(viewsets.ModelViewSet):
    serializer_class = UsertoIndustrySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        industry_id = self.request.query_params.get('industry_id')  # int
        user_id = self.request.query_params.get('user_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'industry_id', industry_id)
        add_to_queryset(queryset_params, 'user_id', user_id)

        if queryset_params:
            return UsertoIndustry.objects.filter(**queryset_params)
        return UsertoIndustry.objects.all()


class UsertoIndustryPostAPI(viewsets.ModelViewSet):
    serializer_class = UsertoIndustrySerializer
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
