from django.shortcuts import render
from django.utils.safestring import mark_safe
from datetime import datetime
from django.views import View
from django.utils import timezone
from datetime import date
from calendar import HTMLCalendar
from itertools import groupby
from .models import Calendar as CalendarModel
from .models import Filter
from events.models import Event
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators import csrf
from django.views.generic.edit import CreateView
from django.utils.html import conditional_escape as esc
from login.views import LoginPermissionMixin

import logging
logger = logging.getLogger(__name__)

class MyCalendar(LoginPermissionMixin, View):
    def get(self, request):
        calendar = CalendarModel.objects.get(user__user=request.user.pk)
        id = calendar.pk
        
        address = '/calendar/' + str(id)
        return HttpResponseRedirect(address)

class EventCalendar(HTMLCalendar):

    def __init__(self, events, calendar):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)
        self.calendar = calendar

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            cssclass += ' day'
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = ['<div class="event-area">']
                for event in self.events[day]:
                    if event.busy_private == False and event.allow_booking == False:
                        event_link = '/event/' + str(event.pk)
                        event_html = '<a href=' + event_link + '>'
                        body.append('<div>')
                        body.append(event_html)
                        body.append(esc(str(event.time.hour) + "-" + event.name))
                        body.append('</a></div>')
                    elif event.busy_private == True:
                        body.append('<div class="busy-private">')
                        body.append(esc("Busy " + str(event.time.hour) + 
                        ":" + str(event.time.minute) + " - " + str(event.end_time.hour) +
                        ":" + str(event.end_time.minute)))
                        body.append('</div>')
                    elif event.allow_booking == True:
                        event_link = '/book_event/' + str(event.pk) + "/" + str(self.calendar.pk)
                        event_html = '<a href=' + event_link + '>'
                        body.append('<div class="allow-booking">')
                        body.append(event_html)
                        body.append(esc("Book time " + str(event.time.hour) + 
                        ":" + str(event.time.minute) + " - " + str(event.end_time.hour) +
                        ":" + str(event.end_time.minute)))
                        body.append('</a></div>')
                body.append('</div>')
                return self.day_cell(cssclass, '%d %s' % (day, '<div></div>'.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

def get_calendar_context(calendar, filter, filter_params, date):
    times = [
            "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM",
            "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
            "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM",
            "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
        ]

    upcoming_events = Event.objects.filter(calendar=calendar, date__gt=timezone.now()).order_by('-date')[:4]
    recent_events = Event.objects.filter(calendar=calendar, date__lt=timezone.now()).order_by('date')[:2]


    context = {
            'calendar': calendar,
            'times': times,
            'filters': filter,
            'date_object': date,
            'filter_params': filter_params,
            'upcoming_events': upcoming_events,
            'recent_events': recent_events
    }  

   
    if filter_params == []:
        events = Event.objects.filter(date__year=date.year, date__month=date.month, calendar=calendar)
        html_c = EventCalendar(events, calendar).formatmonth(date.year, date.month)
        context['html_calendar'] = mark_safe(html_c)
        context['no_params'] = True
    else:
        for i in range(0, len(filter_params)):
            filter_params[i] = int(filter_params[i])
        events = Event.objects.filter(date__year=date.year, date__month=date.month, calendar=calendar, sub_calendar__in=filter_params)
        logger.error(events)
        html_c = EventCalendar(events, calendar).formatmonth(date.year, date.month)
        context['html_calendar'] = mark_safe(html_c)
        context['no_params'] = False

    if calendar.user == None:
        context['member_calendar'] = True
        context['user_calendar'] = False
    elif calendar.member == None:
        context['user_calendar'] = True
        context['member_calendar'] = False
    else:
        context['user_calendar'] = False
        context['member_calendar'] = False

    return context

class Calendar(LoginPermissionMixin, View):
    template_name = 'cal/calendar.html'
    today = datetime.today()

    def get(self, request, pk):

        calendar = CalendarModel.objects.get(pk=pk)
        filters = Filter.objects.filter(calendar=calendar)
        filter_params = request.GET.getlist('filters')
        today = datetime.today()
        context = get_calendar_context(calendar, filters, filter_params, today)

        return render(request, self.template_name, context)

class CalendarDate(LoginPermissionMixin, View):
    template_name = 'cal/calendar.html'

    def get(self, request, pk, year, month):
        c = CalendarModel.objects.get(pk=pk)
        f = Filter.objects.filter(calendar=c)
        today = datetime.today()
        new_date = today.replace(year=year, month=month)
        
        context = get_calendar_context(c, f, new_date)

        return render(request, self.template_name, context)

class CreateFilter(LoginPermissionMixin, CreateView):
    template_name = 'create_edit_model.html'
    model = Filter
    fields = ('name',)

    def get_context_data(self, **kwargs):
        context = super(CreateFilter, self).get_context_data(**kwargs)
        context['button_text'] = 'Create Calendar'
        return context

    def dispatch(self, *args, **kwargs):
        return super(CreateFilter, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        cal_pk = self.kwargs.get('pk')
        cal = CalendarModel.objects.get(pk=cal_pk)
        obj.calendar = cal
        obj.save() 

        success_url = "/calendar/" + str(cal_pk)
        return HttpResponseRedirect(success_url)
    

@csrf.csrf_exempt
def create_event(request):
   
    return HttpResponse('success')
