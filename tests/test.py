from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client, TestCase

from band_main.models import Song, Event, Organizator
from band_main.views import HomeView


import pytest


def test_home_view():
    url = reverse('home')
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


