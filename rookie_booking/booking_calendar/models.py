from django.db import models
from django.utils import timezone

from rookie_booking.userprofile.models import User


class Location(models.Model):
    name        = models.CharField(blank=False, max_length=30,  default="",)
    description = models.CharField(blank=True,  max_length=100, default="",)
    color       = models.CharField(blank=False, max_length=10, )

    def __str__(self):
        return self.name.encode('utf-8')


class Booking(models.Model):
    user            = models.ForeignKey(to=User,     related_name='bookings', blank=True)
    location        = models.ForeignKey(to=Location, related_name='bookings', blank=False)
    description     = models.CharField(blank=True,  max_length=100, default="")
    start_date_time = models.DateTimeField("Start", blank=False)
    end_date_time   = models.DateTimeField("End",   blank=False)


class PoolResult(models.Model):
    winner     = models.ForeignKey(to=User, related_name='winning_games', blank=False)
    loser      = models.ForeignKey(to=User, related_name='losing_games',  blank=False)
    balls_left = models.PositiveSmallIntegerField("Loser Balls Left",     blank=False, default=1)
    created_by = models.ForeignKey(to=User)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} v {1} - {2}".format(self.winner, self.loser, self.created_on)


class SpeedRun(models.Model):
    person      = models.ForeignKey(verbose_name="Contender", to=User, related_name='speed_runs', blank=False)
    verified_by = models.ForeignKey(to=User, related_name='speed_run_verifications', blank=False)
    time        = models.TimeField("Time",     blank=False, default=1)
    created_by  = models.ForeignKey(to=User)
    created_on  = models.DateTimeField(default=timezone.now)