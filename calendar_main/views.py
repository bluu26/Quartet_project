from django.shortcuts import render, redirect
from django.views import View
import calendar
from datetime import date, datetime
from django.utils import timezone

from django.views.generic import TemplateView

from band_main.models import Event, Song, Organizator
from calendar_main.forms import EventForm


from django.utils import timezone
import calendar

class CalendarView(TemplateView):
    template_name = 'calendar/calendar_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year', timezone.now().year)
        month = self.kwargs.get('month', timezone.now().month)
        context['year'] = year
        context['month'] = month

        context['current_month'] = timezone.datetime(year, month, 1).strftime('%B %Y')

        context['month_days'] = self.get_month_days(year, month)
        context['event_dict'] = self.get_event_dict(year, month)

        previous_month_date = (timezone.datetime(year, month, 1) - timezone.timedelta(days=1)).replace(day=1)
        next_month_date = (timezone.datetime(year, month, 1) + timezone.timedelta(days=calendar.monthrange(year, month)[1])).replace(day=1)

        context['previous_month'] = previous_month_date
        context['next_month'] = next_month_date

        return context

    def get_month_days(self, year, month):
        month_calendar = calendar.monthcalendar(year, month)
        month_days = []
        for week in month_calendar:
            week_days = []
            for day in week:
                if day == 0:
                    week_days.append(None)
                else:
                    week_days.append(day)
            month_days.append(week_days)
        return month_days

    def get_event_dict(self, year, month):
        events = Event.objects.filter(date_start__year=year, date_start__month=month)
        event_dict = {}

        for event in events:
            day = event.date_start.day
            day_of_week = event.date_start.strftime('%A')

            if (day, day_of_week) not in event_dict:
                event_dict[(day, day_of_week)] = []

            event_dict[(day, day_of_week)].append(event.event_name)
        print(event_dict)
        print(event_dict[(day, day_of_week)])
        return event_dict


class AddEventView(View):
    template_name = 'create_event.html'

    def get(self, request, day, month, year):
        form = EventForm(initial={'date_start': date(year, month, day)})
        songs = Song.objects.all()
        organizators = Organizator.objects.all()
        context = {
            'form': form,
            'songs': songs,
            'organizators': organizators
        }
        return render(request, self.template_name, context)

    def post(self, request, day, month, year):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.date_start = date(year, month, day)  # Ustawienie daty rozpoczęcia na podstawie URL
            event.save()
            form.save_m2m()  # Zapisanie relacji Many-to-Many

            # Dodaj utwory do wydarzenia
            song_ids = request.POST.getlist('songs')
            for song_id in song_ids:
                event.song.add(Song.objects.get(id=song_id))

            return redirect('calendar_view', year=year, month=month)

        songs = Song.objects.all()
        organizators = Organizator.objects.all()
        context = {
            'form': form,
            'songs': songs,
            'organizators': organizators
        }
        return render(request, self.template_name, context)
