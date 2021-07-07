from rest_framework import viewsets
from .models import SearchObject
from .models import SearchTags
from .serializers import SearchObjectSerializer
from .serializers import SearchTagsSerializer


class SearchObjectAPI(viewsets.ModelViewSet):
    serializer_class = SearchObjectSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = SearchObject.objects.all()


class SearchTagsAPI(viewsets.ModelViewSet):
    serializer_class = SearchTagsSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = SearchTags.objects.all()
