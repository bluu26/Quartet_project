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

