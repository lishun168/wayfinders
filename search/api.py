from django.core.exceptions import PermissionDenied
from requests import Response
from rest_framework import viewsets, permissions

from members.models import MemberUser
from .models import SearchObject
from .models import SearchTags
from .serializers import SearchObjectSerializer
from .serializers import SearchTagsSerializer
from wayfinders.functions import add_to_queryset


class SearchObjectAPI(viewsets.ModelViewSet):
    serializer_class = SearchObjectSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        reference_type = self.request.query_params.get('reference_type')  # int
        url = self.request.query_params.get('url')  # int
        description = self.request.query_params.get('description')

        queryset_params = {}
        add_to_queryset(queryset_params, 'reference_type', reference_type)
        add_to_queryset(queryset_params, 'url', url)
        add_to_queryset(queryset_params, 'description__icontains', description)

        if queryset_params:
            return SearchObject.objects.filter(**queryset_params)
        return SearchObject.objects.all()


class SearchObjectPostAPI(viewsets.ModelViewSet):
    serializer_class = SearchObjectSerializer
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


class SearchTagsAPI(viewsets.ModelViewSet):
    serializer_class = SearchTagsSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        search_object_id = self.request.query_params.get('search_object_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'tag__icontains', tag)
        add_to_queryset(queryset_params, 'search_object_id', search_object_id)

        if queryset_params:
            return SearchTags.objects.filter(**queryset_params)
        return SearchTags.objects.all()


class SearchTagsPostAPI(viewsets.ModelViewSet):
    serializer_class = SearchTagsSerializer
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
