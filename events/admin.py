from django.contrib import admin
from .models import Event
from .models import Invitation
from .models import Participants
from .models import EventType

class ParticipantInline(admin.TabularInline):
    model = Participants

class EventAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Invitation)
admin.site.register(Participants)
admin.site.register(EventType)