from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from band_main.models import Song, Organizator, Event


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class CreateEventView(View):
    def get(self, request):
        songs = Song.objects.all()
        organizators = Organizator.objects.all()
        context = {'songs': songs, 'organizators': organizators}
        return render(request, 'create_event.html', context)

    def post(self, request):
        event_name = request.POST.get('event_name')
        date_start = request.POST.get('date_start')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')
        location = request.POST.get('location')
        money_profit = request.POST.get('money_profit')
        description = request.POST.get('description')
        organizator_id = request.POST.get('organizer_id')

        organizator = get_object_or_404(Organizator, id=organizator_id)

        event = Event.objects.create(
            event_name=event_name,
            date_start=date_start,
            time_start=time_start,
            time_end=time_end,
            location=location,
            money_profit=money_profit,
            description=description,
            organizator=organizator
        )

        song_ids = request.POST.getlist('songs')
        for song_id in song_ids:
            song = get_object_or_404(Song, id=song_id)
            event.songs.add(song)

        return redirect('success_page')


