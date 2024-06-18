from django import forms
from .models import Event, Organizator, Song


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'event_name', 'date_start', 'time_start', 'time_end',
            'localization', 'money_profit', 'description',
            'song', 'leaving_location', 'leaving_time', 'organizator'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Opis'}),
        }

    song = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class OrganizatorForm(forms.ModelForm):
    class Meta:
        model = Organizator
        fields = ['name', 'contact', 'description']
