from django import forms
from band_main.models import Event, Song


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'date_start', 'time_start', 'time_end', 'localization', 'money_profit',
                  'description', 'leaving_location', 'leaving_time', 'organizator', 'song']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['song'].widget = forms.CheckboxSelectMultiple()

        # Pobierz wszystkie dostępne piosenki
        self.fields['song'].queryset = Song.objects.all()
