from django.contrib import admin
from django.urls import path

from band_main import views

urlpatterns = [
    path('createevent/', views.CreateEventView.as_view(), name='create_event'),
    path('event_details/<int:pk>', views.EventDetailsView.as_view(), name='event_details'),
    path('addsong/', views.AddSongView.as_view(), name='add_song'),
    path('songlist/', views.SongListView.as_view(), name='song_list'),
    path('successpage/', views.SuccessPageView.as_view(), name='success_page'),
    path('addorganizator/', views.AddOrganizatorView.as_view(), name='add_organizator'),
    path('organizator_list/', views.OrganizatorListView.as_view(), name='organizator_list'),

]
