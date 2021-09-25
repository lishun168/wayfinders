from django.core.exceptions import PermissionDenied
from requests import Response
from rest_framework import viewsets
from members.models import MemberUser
from .models import Calendar
from .models import Filter
from .serializers import CalendarSerializer
from .serializers import FilterSerializer
from wayfinders.functions import add_to_queryset

class CalendarAPI(viewsets.ModelViewSet):
    serializer_class = CalendarSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        public = self.request.query_params.get('public')  # bool
        name = self.request.query_params.get('name')
        member_id = self.request.query_params.get('member_id')  # int
        user_id = self.request.query_params.get('user_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'member_id', member_id)
        add_to_queryset(queryset_params, 'user_id', user_id)

        if (public == "true"):
            add_to_queryset(queryset_params, 'public', True)
        elif (public == "false"):
            add_to_queryset(queryset_params, 'public', False)

        if queryset_params:
            return Calendar.objects.filter(**queryset_params)
        return Calendar.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        member_user = MemberUser.objects.get(user=user)
        instance = serializer.data

        if instance.user.user == user or user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if instance.user.user == user or user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

class FilterAPI(viewsets.ModelViewSet):
    serializer_class = FilterSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        name = self.request.query_params.get('name')
        calendar_id = self.request.query_params.get('calendar_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'calendar_id', calendar_id)

        if queryset_params:
            return Filter.objects.filter(**queryset_params)
        return Filter.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        member_user = MemberUser.objects.get(user=user)
        instance = serializer.data

        if instance.calendar.user.user == user or user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if instance.calendar.user.user == user or user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()
