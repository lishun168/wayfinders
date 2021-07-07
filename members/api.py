from rest_framework import viewsets
from .serializers import MemberSerializer
from .serializers import MemberUserSerializer
from .serializers import UserToMemberSerializer
from .serializers import PermissionsSerializer
from .serializers import UserRoleSerializer
from .serializers import GallerySerializer
from .serializers import ApplicationSerializer
from .models import Member
from .models import MemberUser
from .models import UserToMember
from .models import Permissions
from .models import UserRole
from .models import Gallery
from .models import Application


class MemberAPI(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Member.objects.all()

class MemberUserAPI(viewsets.ModelViewSet):
    serializer_class = MemberUserSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = MemberUser.objects.all()

class UserToMemberAPI(viewsets.ModelViewSet):
    serializer_class = UserToMemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = UserToMember.objects.all()

class PermissionsAPI(viewsets.ModelViewSet):
    serializer_class = PermissionsSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Permissions.objects.all()

class UserRoleAPI(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = UserRole.objects.all()

class GalleryAPI(viewsets.ModelViewSet):
    serializer_class = GallerySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Gallery.objects.all()

class ApplicationAPI(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Application.objects.all()
