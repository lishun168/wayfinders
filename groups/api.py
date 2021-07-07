from rest_framework import viewsets
from .models import Groups
from .models import Rules
from .models import GroupToMember
from .serializers import GroupsSerializer
from .serializers import RulesSerializer
from .serializers import GroupToMemberSerializer


class GroupsAPI(viewsets.ModelViewSet):
    serializer_class = GroupsSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Groups.objects.all()


class RulesAPI(viewsets.ModelViewSet):
    serializer_class = RulesSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Rules.objects.all()


class GroupToMemberAPI(viewsets.ModelViewSet):
    serializer_class = GroupToMemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = GroupToMember.objects.all()