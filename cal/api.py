from rest_framework import viewsets
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

