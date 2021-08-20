from requests import Response
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from members.models import MemberUser
from .models import Event
from .models import Invitation
from .models import Participants
from .models import GuestParticipant
from .serializers import EventSerializer
from .serializers import InvitationSerializer
from .serializers import ParticipantsSerializer
from .serializers import GuestParticipantSerializer
from wayfinders.functions import add_to_queryset


class EventAPI(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    http_method_names = ['get', 'head', 'post', 'patch']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        description = self.request.query_params.get('description')
        date = self.request.query_params.get('date')
        time = self.request.query_params.get('time')
        end_time = self.request.query_params.get('end_time')
        public = self.request.query_params.get('public')  # bool
        is_open = self.request.query_params.get('is_open')  # bool
        open_editing = self.request.query_params.get('open_editing')  # bool
        calender_id = self.request.query_params.get('calender_id')  # int
        search_tag_id = self.request.query_params.get('search_tag_id')  # int
        sub_calender_id = self.request.query_params.get('sub_calender_id')  # int
        allow_booking = self.request.query_params.get('allow_booking')  # bool
        booking_interval_minutes = self.request.query_params.get('booking_interval_minutes')  # int
        booking_interval_buffer = self.request.query_params.get('booking_interval_buffer')  # int
        busy_private = self.request.query_params.get('busy_private')  # bool
        location = self.request.query_params.get('location')

        queryset_params = {}
        add_to_queryset(queryset_params, 'name__icontains', name)
        add_to_queryset(queryset_params, 'description__icontains', description)
        add_to_queryset(queryset_params, 'date__icontains', date)
        add_to_queryset(queryset_params, 'time__icontains', time)
        add_to_queryset(queryset_params, 'end_time__icontains', end_time)
        add_to_queryset(queryset_params, 'calender_id', calender_id)
        add_to_queryset(queryset_params, 'search_tag_id', search_tag_id)
        add_to_queryset(queryset_params, 'sub_calender_id', sub_calender_id)
        add_to_queryset(queryset_params, 'booking_interval_minutes', booking_interval_minutes)
        add_to_queryset(queryset_params, 'booking_interval_buffer', booking_interval_buffer)
        add_to_queryset(queryset_params, 'location__icontains', location)

        if (public == "true"):
            add_to_queryset(queryset_params, 'public', True)
        elif (public == "false"):
            add_to_queryset(queryset_params, 'public', False)

        if (is_open == "true"):
            add_to_queryset(queryset_params, 'is_open', True)
        elif (is_open == "false"):
            add_to_queryset(queryset_params, 'is_open', False)

        if (open_editing == "true"):
            add_to_queryset(queryset_params, 'open_editing', True)
        elif (open_editing == "false"):
            add_to_queryset(queryset_params, 'open_editing', False)

        if (allow_booking == "true"):
            add_to_queryset(queryset_params, 'allow_booking', True)
        elif (allow_booking == "false"):
            add_to_queryset(queryset_params, 'allow_booking', False)

        if (busy_private == "true"):
            add_to_queryset(queryset_params, 'busy_private', True)
        elif (busy_private == "false"):
            add_to_queryset(queryset_params, 'busy_private', False)

        if queryset_params:
            return Event.objects.filter(**queryset_params)
        return Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if member_user.id == request.data.get('created_by') or user.is_superuser or member_user.is_wf_admin:
            self.perform_create(serializer)
            return Response(serializer.data)
        raise PermissionDenied()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        member_user = MemberUser.objects.get(user=user)

        if member_user == instance.created_by or user.is_superuser or member_user.is_wf_admin:
            self.perform_update(serializer)
            return Response(serializer.data)
        raise PermissionDenied()


class InvitationAPI(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        accept = self.request.query_params.get('accept')  # bool
        decline = self.request.query_params.get('decline')  # bool
        events_id = self.request.query_params.get('events_id')  # int
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'events_id', events_id)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if (accept == "true"):
            add_to_queryset(queryset_params, 'accept', True)
        elif (accept == "false"):
            add_to_queryset(queryset_params, 'accept', False)

        if (decline == "true"):
            add_to_queryset(queryset_params, 'decline', True)
        elif (decline == "false"):
            add_to_queryset(queryset_params, 'decline', False)

        if queryset_params:
            return Invitation.objects.filter(**queryset_params)
        return Invitation.objects.all()


class ParticipantsAPI(viewsets.ModelViewSet):
    serializer_class = ParticipantsSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        is_administrator = self.request.query_params.get('name')  # bool
        events_id = self.request.query_params.get('events_id')  # int
        member_id = self.request.query_params.get('member_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'events_id', events_id)
        add_to_queryset(queryset_params, 'member_id', member_id)

        if (is_administrator == "true"):
            add_to_queryset(queryset_params, 'is_administrator', True)
        elif (is_administrator == "false"):
            add_to_queryset(queryset_params, 'is_administrator', False)

        if queryset_params:
            return Participants.objects.filter(**queryset_params)
        return Participants.objects.all()


class GuestParticipantAPI(viewsets.ModelViewSet):
    serializer_class = GuestParticipantSerializer
    http_method_names = ['get', 'head', 'post', 'put']

    def get_queryset(self):
        guest_name = self.request.query_params.get('guest_name')
        guest_email = self.request.query_params.get('guest_email')
        events_id = self.request.query_params.get('events_id')  # int

        queryset_params = {}
        add_to_queryset(queryset_params, 'guest_name__icontains', guest_name)
        add_to_queryset(queryset_params, 'guest_email__icontains', guest_email)
        add_to_queryset(queryset_params, 'events_id', events_id)

        if queryset_params:
            return GuestParticipant.objects.filter(**queryset_params)
        return GuestParticipant.objects.all()