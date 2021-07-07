from django.contrib import admin
from .models import Event, Invitation, Participants

class ParticipantInline(admin.TabularInline):
    model = Participants

class EventAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Invitation)
admin.site.register(Participants)