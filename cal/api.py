from rest_framework import viewsets
from .models import Calendar
from .models import Filter
from .serializers import CalendarSerializer
from .serializers import FilterSerializer

class CalendarAPI(viewsets.ModelViewSet):
    serializer_class = CalendarSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Calendar.objects.all()

class FilterAPI(viewsets.ModelViewSet):
    serializer_class = FilterSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Filter.objects.all()

