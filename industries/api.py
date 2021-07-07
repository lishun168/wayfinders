from rest_framework import viewsets
from .models import Industry
from .models import MemberToIndustry
from .models import UsertoIndustry
from .serializers import IndustrySerializer
from .serializers import MemberToIndustrySerializer
from .serializers import UsertoIndustrySerializer

class IndustryAPI(viewsets.ModelViewSet):
    serializer_class = IndustrySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Industry.objects.all()

class MemberToIndustryAPI(viewsets.ModelViewSet):
    serializer_class = MemberToIndustrySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = MemberToIndustry.objects.all()

class UsertoIndustryAPI(viewsets.ModelViewSet):
    serializer_class = UsertoIndustrySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = UsertoIndustry.objects.all()