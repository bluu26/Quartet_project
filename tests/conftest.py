from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User

from band_main.models import Song, Organizator, Event


@pytest.fixture
def user():
    return User.objects.create(username='test')


@pytest.fixture
def event():
    organizator = Organizator.objects.create(name='org testowy')
    song1 = Song.objects.create(name='song1')
    song2 = Song.objects.create(name='song2')

    event = Event.objects.create(
        event_name='Wydarzenie testowe',
        date_start=datetime.now().date(),
        time_start=datetime.now().time(),
        time_end=(datetime.now() + timedelta(hours=1)).time(),
        localization="testowo",
        money_profit=100.0,
        description='jakiś tekst',
        leaving_time=datetime.now().time(),
        leaving_location='zakopane',
        organizator=organizator
    )
    event.song.add(song1, song2)

    return event


@pytest.fixture
def user_login():
    username = 'test_logggg'
    password = 'yolo'
    return User.objects.create_user(username=username, password=password)


@pytest.fixture
def songs():
    lst = []
    for i in range(5):
        lst.append(Song.objects.create(name=i, composer=i))
    return lst


@pytest.fixture
def organizators():
    lst = []
    for i in range(5):
        lst.append(Organizator.objects.create(name=i, contact=i, description=i))
    return lst

# --------------------------------------------#
# DETAILS EVENTS
# --------------------------------------------#


@pytest.fixture
def organizator2():
    return Organizator.objects.create(name='Organizator 1', contact='Kontakt 1', description='Opis 1')


@pytest.fixture
def songs2():
    return [
        Song.objects.create(name='Song 1', composer='Composer 1'),
        Song.objects.create(name='Song 2', composer='Composer 2')
    ]


@pytest.fixture
def event2(organizator2, songs2):
    event2 = Event.objects.create(
        event_name='Event 1',
        date_start='2024-01-01',
        time_start='12:00',
        time_end='14:00',
        localization='Lokalizacja 1',
        money_profit=100.0,
        description='Opis 1',
        leaving_location='Miejsce wyjazdu 1',
        leaving_time='10:00',
        organizator=organizator2
    )
    event2.song.set(songs2)
    return event2
