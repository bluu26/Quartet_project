from django.urls import path

from band_main.views import CreateEventView
from .views import CalendarView

urlpatterns = [
    path('calendar/<int:year>/<int:month>/', CalendarView.as_view(), name='calendar_view'),
    # path('add_event/<int:day>/<int:month>/<int:year>/', AddEventView.as_view(), name='add_event_view'),
    path('create_event/', CreateEventView.as_view(), name='create_event'),
]

