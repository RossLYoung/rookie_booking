from django.db import models

from rookie_booking.userprofile.models import User


class Location(models.Model):
    name        = models.CharField(blank=False, max_length=30,  default="",)
    description = models.CharField(blank=False, max_length=100, default="",)
    color       = models.CharField(blank=False, max_length=10, )


class Booking(models.Model):
    user            = models.ForeignKey(to=User,     related_name='bookings')
    location        = models.ForeignKey(to=Location, related_name='bookings')
    start_date_time = models.DateTimeField()
    end_date_time   = models.DateTimeField()