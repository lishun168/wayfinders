from django import forms
from django.forms.models import inlineformset_factory
from .models import Event
from .models import Filter

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'location', 'date', 'time', 'end_time', 'public', 'sub_calendar', 'is_open', 'open_editing')

    def __init__(self, *args, **kwargs):
        calendar_pk = kwargs.pop('pk')
        super(EventForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        self.fields['sub_calendar'].queryset = Filter.objects.filter(calendar__pk=calendar_pk)


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'location', 'date', 'time', 'end_time', 'public', 'sub_calendar', 'is_open', 'open_editing')

    def __init__(self, *args, **kwargs):
        event_pk = kwargs.pop('pk')
        event = Event.objects.get(pk=event_pk)
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False

        self.fields['sub_calendar'].queryset = Filter.objects.filter(calendar=event.calendar)