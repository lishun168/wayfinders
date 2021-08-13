import math
from django import forms
from datetime import datetime
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.forms.widgets import SelectDateWidget, TimeInput
from django.views.generic.edit import CreateView, UpdateView
from login.views import LoginPermissionMixin
from cal.models import Calendar
from .models import Invitation, Event, Participants, GuestParticipant
from members.models import MemberUser
from search.models import SearchObject, SearchTags
from .forms import EventForm
from .forms import EventUpdateForm

import logging
logger = logging.getLogger(__name__)

class CreateInvitation(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Invitation
    fields = ('member',)

    def get_context_data(self, **kwargs):
        context = super(CreateInvitation, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Invitation'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateInvitation, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_pk)
        obj.events = event
        obj.save()

        
        success_url = '/event/' + str(event_pk)
        return HttpResponseRedirect(success_url)

class Invite(LoginPermissionMixin, View):
    template_name = 'events/invite.html'
    
    def get(self, request, pk):
        invite = Invitation.objects.get(pk=pk)
        event = Event.objects.get(pk=invite.events.pk)
        participants = Participants.objects.filter(events=event)
        invitations = Invitation.objects.filter(events=event)

        context = {
            'invite': invite,
            'event': event,
            'participants': participants,
            'invitations': invitations
        }

        return render(request, self.template_name, context)

def accept_view(request, invite_pk):
    invite = Invitation.objects.get(pk=invite_pk)
    invite.accept = True
    invite.decline = False
    invite.save()

    participant = Participants()
    participant.events = invite.events
    participant.member = invite.member
    participant.save()

    success_url = '/profile/' + str(invite.member.pk)
    return HttpResponseRedirect(success_url)
    

def decline_view(request, invite_pk):
    invite = Invitation.objects.get(pk=invite_pk)
    invite.decline = True
    invite.accept = False
    invite.save()

    try:
        participant = Participants.objects.get(events=invite.events, member=invite.member)
        participant.delete()
    except Participants.DoesNotExist:
        empty_var = 1

    success_url = '/profile/' + str(invite.member.pk)
    return HttpResponseRedirect(success_url)

def join_view(request, event_pk, user_pk):
    member = MemberUser.objects.get(user=user_pk)
    event = Event.objects.get(event=event_pk)

    participant = Participants()
    participant.member = member
    participant.events = event
    participant.save()

    success_url = '/event/' + str(event_pk)
    return HttpResponseRedirect(success_url)

class CreateEvent(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Event
    form_class = EventForm

    def get_form(self):
        form = super(CreateEvent, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateEvent, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Event'
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateEvent, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = Calendar.objects.get(pk=cal_pk)
        obj.calendar = cal  
        obj.save() 

        member = MemberUser.objects.get(user=self.request.user)
        part = Participants()
        part.member = member
        part.events = obj
        part.is_administrator = True
        part.save()

        search_object = SearchObject()

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class CreateBooking(CreateView):
    template_name = 'create_edit_model.html'
    model = Event
    fields = ('location', 'description', 'event_type', 'date', 'time',  'end_time', 'booking_interval_minutes', 'booking_interval_buffer')

    def get_form(self):
        form = super(CreateBooking, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateBooking, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Booking Times'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateBooking, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = Calendar.objects.get(pk=cal_pk)
        obj.calendar = cal  
        interval = obj.booking_interval_minutes + obj.booking_interval_buffer
        hourly_length_in_minutes = (obj.end_time.hour - obj.time.hour) * 60
        minutes = (obj.end_time.minute - obj.time.minute)
        length = hourly_length_in_minutes + minutes
        sessions = int(length / interval)
        if sessions is 0:
            sessions = 1
        for s in range (0, sessions):
            add_time = interval * s
            add_hours = get_hours(0, add_time)
            start_minute = add_time - (add_hours * 60)
            new_obj = Event()
            new_obj = obj

            #TODO Doesnt account for day change, month change, year change
            start_hour = new_obj.time.hour + add_hours
            new_obj.time.replace(hour = start_hour, minute = start_minute)
            new_obj.end_time = obj.end_time
            end_add_minutes = new_obj.end_time.minute + interval
            
            end_add_hours = get_hours(0, end_add_minutes)
            end_minute = end_add_minutes - (end_add_hours * 60)
            
            end_hour = new_obj.end_time.hour + end_add_hours
            new_obj.end_time.replace(hour=end_hour, minute=end_minute)
            new_obj.allow_booking = True
            new_obj.save()

            member = MemberUser.objects.get(user=self.request.user)
            part = Participants()
            part.member = member
            part.events = new_obj
            part.is_administrator = True
            part.save()

            search_object = SearchObject()

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class MarkBusy(CreateView):
    template_name = 'create_edit_model.html'
    model = Event
    fields = ('date', 'time', 'end_time')

    def get_form(self):
        form = super(MarkBusy, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(MarkBusy, self).get_context_data(**kwargs)
        context['button_text'] = 'Mark Time as Busy'
        return context

    def dispatch(self, *args, **kwargs):
        return super(MarkBusy, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = Calendar.objects.get(pk=cal_pk)
        obj.calendar = cal  
        obj.busy_private = True
        obj.name = "Busy"
        obj.save()
        
        member = MemberUser.objects.get(user=self.request.user)
        part = Participants()
        part.member = member
        part.events = obj
        part.is_administrator = True
        part.save()

        search_object = SearchObject()

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class BookEvent(CreateView):
    template_name = 'create_edit_model.html'
    model = GuestParticipant
    fields = ('guest_name', 'guest_email')

    def get_form(self):
        form = super(BookEvent, self).get_form()
        return form

    def get_context_data(self, **kwargs):
        context = super(BookEvent, self).get_context_data(**kwargs)
        context['button_text'] = 'Book Event'
        return context

    def dispatch(self, *args, **kwargs):
        return super(BookEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('cal_pk')
        event_pk = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_pk)
        obj.events = event
        obj.save() 

        event.busy_private = True
        event.save()

        search_object = SearchObject()

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)

class UpdateEvent(LoginPermissionMixin, UpdateView):
    template_name = 'create_edit_model.html'
    model = Event
    form_class = EventUpdateForm
    success_url = "/"

    def get_form(self):
        today = datetime.today()
        form = super(UpdateEvent, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        form.fields['time'].widget = TimeInput(attrs={'type': 'time'})
        form.fields['end_time'].widget = TimeInput(attrs={'type': 'time'})
        return form

    def get_context_data(self, **kwargs):
        context = super(UpdateEvent, self).get_context_data(**kwargs)
        context['button_text'] = 'Update Event'
        return context

    def get_form_kwargs(self):
        kwargs = super(UpdateEvent, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs

    def dispatch(self, *args, **kwargs):
        return super(UpdateEvent, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('event_pk')
        obj.save()

        success_url = "/calendar/" + str(self.object.calendar.id)
        return HttpResponseRedirect(success_url)

class ViewEvent(LoginPermissionMixin, View):
    template_name = 'events/event.html'
    
    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        invitations = Invitation.objects.filter(events=event)
        participants = Participants.objects.filter(events=event)
        member = MemberUser.objects.get(user=request.user)

        context = {
            'event': event,
            'invitations': invitations,
            'participants': participants
        }

        if event.calendar.user == None:
            context['member_calendar'] = True
            context['user_calendar'] = False
        elif event.calendar.member == None:
            context['user_calendar'] = True
            context['member_calendar'] = False
        else:
            context['user_calendar'] = False
            context['member_calendar'] = False

        try:
            my_participation = Participants.objects.get(events=event, member=member)
            context.update({
                'my_part': True,
                'admin': my_participation.is_administrator
            })
            return render(request, self.template_name, context)
        except Participants.DoesNotExist:
            context.update({
                'my_part': False
            })
            return render(request, self.template_name, context)

def get_hours(hours, minutes):
    if minutes >= 60:
        minutes -= 60
        hours += 1
        return get_hours(hours, minutes)
    else:
        return hours

class CreateParticipant(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Participants
    fields = ('member', 'is_administrator')

    def get_context_data(self, **kwargs):
        context = super(CreateParticipant, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Participant'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateParticipant, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        event_pk = self.kwargs.get('pk')
        event = Event.objects.get(pk=event_pk)
        obj.events = event
        obj.save()

        
        success_url = '/event/' + str(event_pk)
        return HttpResponseRedirect(success_url)

class RemoveParticipant(LoginPermissionMixin, DeleteView):
    template_name = 'create_edit_model.html'
    model = Participants

    def get_context_data(self, **kwargs):
        context = super(RemoveParticipant, self).get_context_data(**kwargs)
        context['button_text'] = 'Remove Participant'
        return context
    
    def dispatch(self, *args, **kwargs):
        return super(RemoveParticipant, self).dispatch(*args, **kwargs)
    
    def delete(self, request, *arg, **kwargs):
        pk = self.kwargs.get('pk')
        event_pk = self.kwargs.get('event_pk')
        
        participant = Participants.objects.get(pk=pk)
        participant.delete()

        success_url = "/event/" + str(event_pk)
        return HttpResponseRedirect(success_url )
            
