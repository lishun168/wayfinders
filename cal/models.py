from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from members.models import MemberUser, Member

class Calendar(models.Model):
    public = models.BooleanField(default=True)
    name = models.CharField(max_length=255, default='')

    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

class Filter(models.Model):
    name = models.CharField(max_length=255)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.calendar, self.name)

