from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from members.models import MemberUser, Member

class Calendar(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=255, default='')
    number_of_flags = models.IntegerField(default=0)
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

class Filter(models.Model):
    name = models.CharField(max_length=255)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

class UserFlagCalendar(models.Model):
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s : %s' % (self.calendar, self.user, self.flagged)
