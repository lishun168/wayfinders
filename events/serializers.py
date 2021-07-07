from rest_framework import serializers
from .models import Event
from .models import Invitation
from .models import Participants
from .models import GuestParticipant


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'


class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = '__all__'

class GuestParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestParticipant
        fields = '__all__'
