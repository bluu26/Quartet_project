from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from band_main.models import Event

from django.utils import timezone
import calendar


class CalendarView(LoginRequiredMixin, TemplateView):
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
            if day not in event_dict:
                event_dict[day] = []
            event_dict[day].append(event)
        print("Events:", event_dict)
        return event_dict

