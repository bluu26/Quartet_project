from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

from band_main.models import Song, Event, Organizator
from band_main.views import HomeView


import pytest

from calendar_main.views import CalendarView


def test_home_view():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


def test_about_view():
    url = reverse('about')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200

# --------------------------------------------#
# SUCCESS_PAGE
# --------------------------------------------#


def test_success_page_view():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


# --------------------------------------------#
# ADD_SONG
# --------------------------------------------#

def test_add_song_view_get():
    url = reverse('add_song')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_song_view_get_login(user):
    url = reverse('add_song')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_song_view_post(user):
    url = reverse('add_song')
    client = Client()
    client.force_login(user)
    data = {
        'name': 'Song',
        'composer': 'Jasiu'
    }
    response = client.post(url, data)
    song = Song.objects.get(name='Song', composer='Jasiu')

    assert song
    assert response.status_code == 302


# --------------------------------------------#
# SONG_LIST
# --------------------------------------------#


@pytest.mark.django_db
def test_song_list_view(client, user):
    client.force_login(user)
    url = reverse('song_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_song_list_len(client, user, songs):
    client.force_login(user)
    url = reverse('song_list')
    response = client.get(url)
    assert response.status_code == 200
    song_objects = response.context['songs']
    assert song_objects.count() == len(songs)
    for s in songs:
        assert s in song_objects


@pytest.mark.django_db
def test_edit_song_view(client, user, songs2):
    client.force_login(user)
    song = songs2[0]
    url = reverse('edit_song', args=[song.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].instance == song
    assert response.context['song'] == song


@pytest.mark.django_db
def test_edit_song_view_success(client, user, songs2):
    client.force_login(user)
    song = songs2[0]
    url = reverse('edit_song', args=[song.id])
    data = {
        'name': 'new name',
        'composer': 'new composer'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('song_list')

    song.refresh_from_db()
    assert song.name == 'new name'
    assert song.composer == 'new composer'


@pytest.mark.django_db
def test_edit_song_view_fail(client, user, songs2):
    client.force_login(user)
    song = songs2[0]
    url = reverse('edit_song', args=[song.id])
    data = {
        'name': '',
        'composer': 'new composer'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
    assert response.context['song'] == song

    song.refresh_from_db()
    assert song.name != ''
    assert song.composer != 'new composer'


@pytest.mark.django_db
def test_delete_song_view_get(client, user, song_del):
    client.force_login(user)
    url = reverse('delete_song', args=[song_del.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'song' in response.context
    assert response.context['song'] == song_del


@pytest.mark.django_db
def test_delete_song_view_post(client, user, song_del):
    client.force_login(user)
    url = reverse('delete_song', args=[song_del.id])
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse('song_list')

    with pytest.raises(Song.DoesNotExist):
        Song.objects.get(id=song_del.id)

# --------------------------------------------#
# ORGANIZATOR
# --------------------------------------------#


@pytest.mark.django_db
def test_add_organizator_view_get(user):
    url = reverse('add_organizator')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_organizator_view_post(client, user):
    client.force_login(user)
    url = reverse('add_organizator')
    data = {
        'name': 'orgtest',
        'contact': '567678987',
        'description': 'bogacz'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('success_page')
    assert Organizator.objects.filter(name='orgtest').exists()


@pytest.mark.django_db
def test_add_organizator_view_post_logout(client):
    url = reverse('add_organizator')
    data = {
        'name': 'orgtest',
        'contact': '567678987',
        'description': 'bogacz'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))
    assert not Organizator.objects.filter(name='orgtest').exists()


@pytest.mark.django_db
def test_edit_organizator_view_get(client, user, organizator2):
    client.force_login(user)
    url = reverse('edit_organizator', args=[organizator2.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].instance == organizator2


@pytest.mark.django_db
def test_edit_organizator_view_post(client, user, organizator2):
    client.force_login(user)
    url = reverse('edit_organizator', args=[organizator2.id])
    data = {
        'name': 'new name',
        'contact': 'new contact',
        'description': 'new description'
    }
    response = client.post(url, data)
    organizator2.refresh_from_db()
    assert response.status_code == 302
    assert response.url == reverse('organizator_list')

    assert organizator2.name == 'new name'
    assert organizator2.contact == 'new contact'
    assert organizator2.description == 'new description'


@pytest.mark.django_db
def test_delete_organizator_view_get(client, user, organizator2):
    client.force_login(user)
    url = reverse('delete_organizator', args=[organizator2.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'delete_organizator.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_delete_organizator_view_post(client, user, organizator2):
    client.force_login(user)
    url = reverse('delete_organizator', args=[organizator2.id])
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('organizator_list')
    assert not Organizator.objects.filter(id=organizator2.id).exists()

# --------------------------------------------#
# ORGANIZATOR_LIST
# --------------------------------------------#


@pytest.mark.django_db
def test_organizator_view_authorized_get(client, user):
    client.force_login(user)
    url = reverse('organizator_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_organizator_view_unauthorized_get(client):
    url = reverse('organizator_list')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_organizator_list_view(client, user, organizators):
    client.force_login(user)
    url = reverse('organizator_list')
    response = client.get(url)
    assert response.status_code == 200
    organizators_objects = response.context['organizators']
    assert organizators_objects.count() == len(organizators)
    for s in organizators:
        assert s in organizators_objects


# --------------------------------------------#
# CREATE_EVENT
# --------------------------------------------#


def test_create_event_view_get():
    url = reverse('create_event')
    client = Client()
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_event_view_login(client):
    user = User.objects.create_user(username='test', password='testp')
    client.login(username='test', password='testp')
    url = reverse('create_event')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_event_view_login2(user):
    url = reverse('create_event')
    client = Client()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_event_view_post(user):
    url = reverse('create_event')
    client = Client()
    client.force_login(user)
    organizator = Organizator.objects.create(name='Losowy Organizator')
    songs = Song.objects.create(name='Piosenka 1'), Song.objects.create(name='Piosenka 2')

    data = {
        'event_name': 'Randomowe Wydarzenie',
        'date_start': '1234-12-12',
        'time_start': '12:12',
        'time_end': '12:15',
        'localization': 'Miejsce losowe',
        'money_profit': 123.45,
        'description': 'jakiś opis',
        'leaving_time': '14:15',
        'leaving_location': 'Miejsce zakończenia',
        'organizator_id': organizator.id,
        'songs': [song.id for song in songs]
    }
    response = client.post(url, data)

    assert Event.objects.get(event_name='Randomowe Wydarzenie')
    assert response.status_code == 302
# --------------------------------------------#
# EVENT_DETAILS
# --------------------------------------------#


@pytest.mark.django_db
def test_event_details_view_get(client, user, event2):
    client.force_login(user)
    url = reverse('event_details', kwargs={'pk': event2.pk})
    response = client.get(url)
    assert response.status_code == 200
    result = response.context
    assert result['event'] == event2
    event_context = result['event']
    assert event_context.event_name == event2.event_name
    assert list(event_context.song.all()) == list(event2.song.all())


@pytest.mark.django_db
def test_event_edit_view_post(client, user, event3):
    client.force_login(user)
    url = reverse('event_edit', kwargs={'pk': event3.pk})
    data = {
        'event_name': 'Updated Event Name',
        'date_start': '2024-06-21',
        'time_start': '13:00',
        'time_end': '15:00',
        'localization': 'Updated Localization',
        'money_profit': 200.0,
        'description': 'Updated Description',
        'leaving_location': 'Updated Leaving Location',
        'leaving_time': '11:00',
        'organizator': event3.organizator.pk,
        'song': [song.pk for song in event3.song.all()],
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('success_page')
    event3.refresh_from_db()
    assert event3.event_name == 'Updated Event Name'
    assert str(event3.date_start) == '2024-06-21'
    assert str(event3.time_start) == '13:00:00'
    assert str(event3.time_end) == '15:00:00'
    assert event3.localization == 'Updated Localization'
    assert event3.money_profit == 200.0
    assert event3.description == 'Updated Description'
    assert event3.leaving_location == 'Updated Leaving Location'
    assert str(event3.leaving_time) == '11:00:00'
    assert event3.organizator.pk == event3.organizator.pk
    assert list(event3.song.all()) == list(event3.song.all())


@pytest.mark.django_db
def test_event_delete_view_get(client, user, event3):
    client.force_login(user)
    url = reverse('delete_event', kwargs={'pk': event3.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'object' in response.context
    assert response.context['object'] == event3


@pytest.mark.django_db
def test_event_delete_view_post(client, user, event3):
    client.force_login(user)
    url = reverse('delete_event', kwargs={'pk': event3.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('success_page')
    with pytest.raises(Event.DoesNotExist):
        event3.refresh_from_db()


@pytest.mark.django_db
def test_event_list_view(client, user, event3, event4):
    client.force_login(user)
    url = reverse('event_list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'events' in response.context
    assert event3 in response.context['events']
    assert event4 in response.context['events']

# --------------------------------------------#
# REGISTER
# --------------------------------------------#


@pytest.mark.django_db
def test_register_view_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_view_success(client):
    url = reverse('register')
    data = {
        'username': 'testowy',
        'password': 'pass123',
        'password2': 'pass123',
        'secret_code': '9321'
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('success_page')
    assert User.objects.filter(username='testowy').exists()


@pytest.mark.django_db
def test_register_view_secret_code(client):
    url = reverse('register')
    data = {
        'username': 'testowy',
        'password': 'pass123',
        'password2': 'pass123',
        'secret_code': 'wrongcode'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'accounts/create_user.html' in [t.name for t in response.templates]
    assert 'Błędny kod' in response.context['error']
    assert not User.objects.filter(username='testowy').exists()


@pytest.mark.django_db
def test_register_view_empty_field(client):
    url = reverse('register')
    data = {
        'username': '',
        'password': 'pass123',
        'password2': 'pass123',
        'secret_code': '9321'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert 'accounts/create_user.html' in [t.name for t in response.templates]
    assert 'error' in response.context
    assert not User.objects.filter(username='testowy').exists()

# --------------------------------------------#
# LOGIN & LOGOUT
# --------------------------------------------#


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_success(client, user_login):
    url = reverse('login')
    data = {
        'username': user_login.username,
        'password': 'yolo'

    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('success_page')

    user_login = authenticate(username=user_login.username, password='yolo')
    assert user_login is not None


@pytest.mark.django_db
def test_login_view_failure(client, user_login):
    url = reverse('login')
    data = {
        'username': user_login.username,
        'password': 'baddog'
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse('login')


@pytest.mark.django_db
def test_logout_view(client, user_login):
    client.force_login(user_login)
    url = reverse('logout')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('success_page')
    assert 'auth_user_id' not in client.session


# --------------------------------------------#
# CALENDAR
# --------------------------------------------#

@pytest.mark.django_db
def test_calendar_view_get(client, user):
    client.force_login(user)
    now = timezone.now()
    url = reverse('calendar_view', kwargs={'year': now.year, 'month': now.month})
    response = client.get(url)
    assert response.status_code == 200
    assert 'calendar/calendar_main.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_calendar_view_specific_month(client, user):
    client.force_login(user)
    url = reverse('calendar_view', kwargs={'year': 2024, 'month': 6})
    response = client.get(url)
    assert response.status_code == 200
    context = response.context
    assert context['year'] == 2024
    assert context['month'] == 6
    assert context['current_month'] == 'June 2024'
    assert context['previous_month'].month == 5
    assert context['next_month'].month == 7


@pytest.mark.django_db
def test_get_month_days():
    view = CalendarView()
    days = view.get_month_days(2024, 6)
    assert len(days) == 5
    assert days[0] == [None, None, None, None, None, 1, 2]
    assert days[1] == [3, 4, 5, 6, 7, 8, 9]


@pytest.mark.django_db
def test_get_event_dict(client, user, event3, event4):
    client.force_login(user)

    view = CalendarView()
    event_dict = view.get_event_dict(2024, 6)
    assert len(event_dict) == 2
    assert len(event_dict[20]) == 1
    assert len(event_dict[22]) == 1
    assert event_dict[20][0].event_name == 'Event 1'
    assert event_dict[22][0].event_name == 'Event 2'
