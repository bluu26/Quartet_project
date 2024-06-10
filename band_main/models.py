from django.contrib.auth.models import User
from django.db import models


class Composer(models.Model):
    name = models.CharField(max_length=100)


class Song(models.Model):
    name = models.CharField(max_length=100)
    composer = models.ManyToManyField(Composer)

    def __str__(self):
        return f"{self.composer, self.name}"


class Organizator(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    date_start = models.DateField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    localization = models.CharField(max_length=100)
    money_profit = models.FloatField(default=0.0)
    description = models.TextField()
    song = models.ManyToManyField(Song)
    leaving_location = models.CharField(max_length=100)
    leaving_time = models.CharField(max_length=100)
    organizator = models.ForeignKey(Organizator, on_delete=models.CASCADE)


class DaysOff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    color = models.CharField(max_length=100)


class SummaryMonth(models.Model):
    monthly_events = models.ForeignKey(Event, on_delete=models.CASCADE)
    monthly_profit_total = models.FloatField()


class BandInfo(models.Model):
    musician = models.CharField(max_length=100)
    description = models.TextField()


# class GuestPanel(models.Model):
#     guest_name = models.CharField(max_length=100)
#     guest_email = models.CharField(max_length=100)
#     guest_phone = models.CharField(max_length=100)
#     guest_inquiry = models.CharField(max_length=255)
#     guest_unique_number = models.CharField(max_length=20)
#
#
# class MusicFiles(models.Model):
#     name = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="music/%Y/%m/%d")





    



