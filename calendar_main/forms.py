from django import forms
from band_main.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'date_start', 'time_start', 'time_end', 'localization', 'money_profit', 'description',
                  'song', 'leaving_location', 'leaving_time', 'organizator']
