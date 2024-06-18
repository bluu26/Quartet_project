from django.contrib import admin
from django.urls import path

from band_main import views

urlpatterns = [
    path('createevent/', views.CreateEventView.as_view(), name='create_event'),
    path('event_details/<int:pk>', views.EventDetailsView.as_view(), name='event_details'),
    path('event/edit/<int:pk>/', views.EventEditView.as_view(), name='edit_event'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete_event'),
    path('event/<int:pk>/edit/', views.EventEditView.as_view(), name='event_edit'),
    path('addsong/', views.AddSongView.as_view(), name='add_song'),
    path('songlist/', views.SongListView.as_view(), name='song_list'),
    path('songs/edit/<int:song_id>/', views.EditSongView.as_view(), name='edit_song'),
    path('songs/delete/<int:song_id>/', views.DeleteSongView.as_view(), name='delete_song'),
    path('successpage/', views.SuccessPageView.as_view(), name='success_page'),
    path('addorganizator/', views.AddOrganizatorView.as_view(), name='add_organizator'),
    path('edit/<int:organizator_id>/', views.EditOrganizatorView.as_view(), name='edit_organizator'),
    path('delete/<int:organizator_id>/', views.DeleteOrganizatorView.as_view(), name='delete_organizator'),
    path('organizator_list/', views.OrganizatorListView.as_view(), name='organizator_list'),

]
