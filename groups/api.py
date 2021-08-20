from rest_framework import viewsets
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