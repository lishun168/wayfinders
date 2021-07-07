from django.db import models
from members.models import MemberUser
from cal.models import Calendar, Filter
from datetime import datetime
from search.models import SearchObject

class Event(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(u'Description', blank=True, null=True)
    location = models.TextField(u'Location', blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    date = models.DateField(u'Day of Event')
    time = models.TimeField(u'Start Time')
    end_time = models.TimeField(u'End Time')
    sub_calendar = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Calendar")
    public = models.BooleanField(default=True)
    is_open = models.BooleanField(u'Open to Public', default=False)
    open_editing = models.BooleanField(u'Public can Edit', default=False)
    search_tag = models.ForeignKey(SearchObject, on_delete=models.SET_NULL, blank=True, null=True)
    allow_booking = models.BooleanField(u'Allow Booking',default=False)
    booking_interval_minutes = models.IntegerField(u'Session Length', default=30)
    booking_interval_buffer = models.IntegerField(u'Minutes Between Sessions *optional*', default=0)
    busy_private = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.time))

class Invitation(models.Model):
    member=models.ForeignKey(MemberUser,on_delete=models.CASCADE) #choose the member
    events=models.ForeignKey(Event,on_delete=models.CASCADE) #pull the id of the event
    accept=models.BooleanField(default=False)
    decline=models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.events, self.member)

class Participants(models.Model):
    member=models.ForeignKey(MemberUser,on_delete=models.CASCADE)
    events=models.ForeignKey(Event,on_delete=models.CASCADE)
    is_administrator = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.events, self.member)

    class Meta:
        verbose_name='Participant'
        verbose_name_plural='Participants'

class GuestParticipant(models.Model):
    events = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255)
    guest_email = models.EmailField(max_length=255)

    def __str__(self):
        return '%s %s' % (self.events - self.guest_name)

    class Meta:
        verbose_name='Guest Participant'
        verbose_name_plural='Guest Participants'

