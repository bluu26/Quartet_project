from django.urls import path
from .views import CalendarView, AddEventView

urlpatterns = [
    path('calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='calendar_view'),
    path('add_event/<int:day>/<int:month>/<int:year>/', AddEventView.as_view(), name='add_event_view'),
]

