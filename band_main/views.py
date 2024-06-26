from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

from band_main.forms import EventForm, OrganizatorForm, SongForm
from band_main.models import Song, Organizator, Event


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class SuccessPageView(View):
    def get(self, request):
        return render(request, 'success_page.html')


class AddSongView(LoginRequiredMixin, View):
    def get(self, request):
        messages.success(request, 'Dodano utwór')
        return render(request, 'add_song.html')

    def post(self, request):
        composer = request.POST['composer']
        name = request.POST['name']

        Song.objects.create(name=name, composer=composer)
        return redirect('success_page')


class SongListView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            songs = Song.objects.filter(name__icontains=query)
        else:
            songs = Song.objects.all()
        context = {'songs': songs}
        return render(request, 'song_list.html', context)


class EditSongView(View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        form = SongForm(instance=song)
        return render(request, 'edit_song.html', {'form': form, 'song': song})

    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_list')
        return render(request, 'edit_song.html', {'form': form, 'song': song})


class DeleteSongView(View):
    def get(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        return render(request, 'delete_song.html', {'song': song})

    def post(self, request, song_id):
        song = get_object_or_404(Song, id=song_id)
        song.delete()
        return redirect('song_list')


class AddOrganizatorView(LoginRequiredMixin, View):
    def get(self, request):
        messages.success(request, 'Dodano Organizatora!')
        return render(request, 'add_organizator.html')

    def post(self, request):
        name = request.POST['name']
        contact = request.POST['contact']
        description = request.POST['description']
        Organizator.objects.create(name=name, contact=contact, description=description)
        return redirect('success_page')


class OrganizatorListView(LoginRequiredMixin, View):
    def get(self, request):
        organizators = Organizator.objects.all()
        return render(request, 'organizator_list.html', {'organizators': organizators})


class EditOrganizatorView(UpdateView):
    model = Organizator
    form_class = OrganizatorForm
    template_name = 'edit_organizator.html'
    success_url = reverse_lazy('organizator_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Organizator, pk=self.kwargs['organizator_id'])


class DeleteOrganizatorView(DeleteView):
    model = Organizator
    template_name = 'delete_organizator.html'
    success_url = reverse_lazy('organizator_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Organizator, pk=self.kwargs['organizator_id'])


class CreateEventView(LoginRequiredMixin, View):
    def get(self, request):
        messages.success(request, 'Dodano wydarzenie!')
        songs = Song.objects.all()
        organizators = Organizator.objects.all()
        date_param = request.GET.get('date', 'None')
        print(date_param)
        context = {'songs': songs, 'organizators': organizators, 'date_param': date_param}
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


class EventDetailsView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_details.html'


class EventEditView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('success_page')


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('success_page')


class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.all()

        event_name = self.request.GET.get('event_name')
        if event_name:
            queryset = queryset.filter(event_name__icontains=event_name)

        date_start = self.request.GET.get('date_start')
        if date_start:
            queryset = queryset.filter(date_start=date_start)

        return queryset





