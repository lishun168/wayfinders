from rest_framework import viewsets
from .models import Event
from .models import Invitation
from .models import Participants
from .models import GuestParticipant
from .serializers import EventSerializer
from .serializers import InvitationSerializer
from .serializers import ParticipantsSerializer
from .serializers import GuestParticipantSerializer



class EventAPI(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Event.objects.all()

class InvitationAPI(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Invitation.objects.all()

class ParticipantsAPI(viewsets.ModelViewSet):
    serializer_class = ParticipantsSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Participants.objects.all()

class GuestParticipantAPI(viewsets.ModelViewSet):
    serializer_class = GuestParticipantSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = GuestParticipant.objects.all()
