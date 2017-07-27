import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from rookie_booking.booking_calendar.models import Booking, PoolResult, SpeedRun
from rookie_booking.core.widgets import CustomDateTimePicker, dateAttrs, dateTimeOptions


class AddBookingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddBookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ['description', 'user', 'location', 'start_date_time', 'end_date_time']
        widgets = {
            'start_date_time'  : CustomDateTimePicker(attrs=dateAttrs, options=dateTimeOptions, bootstrap_version=3),
            'end_date_time'    : CustomDateTimePicker(attrs=dateAttrs, options=dateTimeOptions, bootstrap_version=3)
        }

    def clean(self):
        cleaned_data = super(AddBookingForm, self).clean()
        location     = cleaned_data.get("location")
        start        = cleaned_data.get("start_date_time")
        end          = cleaned_data.get("end_date_time")

        if not self.errors:

            if start > end:
                self.add_error('end_date_time', "Must be later than the start date!")

            # >>>>>>>>>>>>>>>>>>>>> time >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # -----------one to compare
            # -----------+++++++++++++++++++++++++++---------------------
            # -----------potential clashes
            # ------++++++++++-------------------------------------------
            # --------------------------------+++++++++++++--------------
            # ----------------+++++++++++++++++--------------------------
            # -----++++++++++++++++++++++++++++++++++++++----------------

            result = []

            overlap_start = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gt=start).exists()
            overlap_end   = Booking.objects.filter(location=location, start_date_time__lt=end,    end_date_time__gte=end).exists()
            outside       = Booking.objects.filter(location=location, start_date_time__gte=start, end_date_time__lte=end).exists()
            inside        = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gte=end).exists()

            if overlap_start or overlap_end or inside or outside:
                if overlap_start:
                    result.append("start overlap")
                if overlap_end:
                    result.append("end overlap")
                if outside:
                    result.append("outside overlap")
                if inside:
                    result.append("inside overlap")

                self.add_error('location', "Occupied!" + " - " + str([x for x in result]))


class EditBookingForm(ModelForm):

    class Meta:
        model = Booking
        fields = ['description', 'user', 'location', 'start_date_time', 'end_date_time']
        widgets = {
            'start_date_time'  : CustomDateTimePicker(attrs=dateAttrs, options=dateTimeOptions, bootstrap_version=3),
            'end_date_time'    : CustomDateTimePicker(attrs=dateAttrs, options=dateTimeOptions, bootstrap_version=3)
        }


    def clean(self):
        cleaned_data = super(EditBookingForm, self).clean()
        location     = cleaned_data.get("location")
        start        = cleaned_data.get("start_date_time")
        end          = cleaned_data.get("end_date_time")

        if not self.errors:

            if start > end:
                self.add_error('end_date_time', "Must be later than the start date!")

            result = []

            overlap_start = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gt=start).exclude(pk=self.instance.id).exists()
            overlap_end   = Booking.objects.filter(location=location, start_date_time__lt=end,    end_date_time__gte=end).exclude(pk=self.instance.id).exists()
            outside       = Booking.objects.filter(location=location, start_date_time__gte=start, end_date_time__lte=end).exclude(pk=self.instance.id).exists()
            inside        = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gte=end).exclude(pk=self.instance.id).exists()

            if overlap_start or overlap_end or inside or outside:
                if overlap_start:
                    result.append("start overlap")
                if overlap_end:
                    result.append("end overlap")
                if outside:
                    result.append("outside overlap")
                if inside:
                    result.append("inside overlap")

                self.add_error('location', "Occupied!" + " - " + str([x for x in result]))



class PoolResultForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PoolResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PoolResult
        fields = ['winner', 'loser', 'balls_left']

    def clean(self):
        cleaned_data   = super(PoolResultForm, self).clean()
        balls_left     = cleaned_data.get("balls_left")
        winner         = cleaned_data.get("winner")
        loser          = cleaned_data.get("loser")
        now            = timezone.now()
        one_minute_ago = now + relativedelta(minutes=-1)

        last_result = PoolResult.objects.last()

        if last_result.created_on > one_minute_ago and winner == last_result.winner and loser == last_result.loser:
            raise ValidationError(
                ValidationError(('This appears to be a duplicate'), code='error1'),
            )

        if balls_left > 7:
            self.add_error('balls_left', "Aye?")

        if winner == loser:
            self.add_error('winner', "Don't be a fud.")
            self.add_error('loser',  "Don't be a fud.")


class PoolSpeedRunForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PoolSpeedRunForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SpeedRun
        fields = ['person', 'time']
