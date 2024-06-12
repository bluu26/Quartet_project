from django.contrib import admin
from django.urls import path

from band_main import views

urlpatterns = [
    path('createevent/', views.CreateEventView.as_view(), name='create_event'),

]
