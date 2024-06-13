from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from band_main.models import Song, Organizator, Event


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class SuccessPageView(View):
    def get(self, request):
        return render(request, 'success_page.html')


class AddSongView(View):
    def get(self, request):
        messages.success(request, 'Dodano utwór')
        return render(request, 'add_song.html')

    def post(self, request):
        composer = request.POST['composer']
        name = request.POST['name']

        Song.objects.create(name=name, composer=composer)
        return redirect('success_page')


class SongListView(View):
    def get(self, request):
        songs = Song.objects.all()
        context = {'songs': songs}
        return render(request, 'song_list.html', context)


class AddOrganizatorView(View):
    def get(self, request):
        return render(request, 'add_organizator.html')

    def post(self, request):
        name = request.POST['name']
        contact = request.POST['contact']
        description = request.POST['description']
        Organizator.objects.create(name=name, contact=contact, description=description)
        return redirect('success_page')


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
        localization = request.POST.get('localization')
        money_profit = request.POST.get('money_profit')
        description = request.POST.get('description')
        organizator_id = request.POST.get('organizator_id')
        leaving_location = request.POST.get('leaving_location')
        leaving_time = request.POST.get('leaving_time')

        organizator = get_object_or_404(Organizator, id=organizator_id)

        event = Event.objects.create(
            event_name=event_name,
            date_start=date_start,
            time_start=time_start,
            time_end=time_end,
            localization=localization,
            money_profit=money_profit,
            description=description,
            organizator=organizator,
            leaving_location=leaving_location,
            leaving_time=leaving_time
        )

        song_ids = request.POST.getlist('songs')
        for song_id in song_ids:
            song = get_object_or_404(Song, id=song_id)
            event.song.add(song)

        return redirect('success_page')


