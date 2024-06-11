from django.urls import reverse
from django.test import Client, TestCase
from band_main.views import HomeView


import pytest


def test_home_view():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200


