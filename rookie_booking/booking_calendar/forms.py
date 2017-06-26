from django.forms import ModelForm

from rookie_booking.booking_calendar.models import Booking, PoolResult
from rookie_booking.core.widgets import CustomDateTimePicker, dateAttrs, dateTimeOptions


class AddBookingForm(ModelForm):

    def __init__(self, *args,**kwargs):
        super (AddBookingForm,self ).__init__(*args,**kwargs)
        # self.user = kwargs.pop('user')

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

            #-----------one to compare
            #-----------+++++++++++++++++++++++++++---------------------
            #-----------potential clashes
            #------++++++++++-------------------------------------------
            #--------------------------------+++++++++++++--------------
            #----------------+++++++++++++++++--------------------------
            #-----++++++++++++++++++++++++++++++++++++++----------------

            overlap_start = Booking.objects.filter(location=location, start_date_time__lt=start, end_date_time__gt=start).exists()
            overlap_end   = Booking.objects.filter(location=location, start_date_time__lt=end,   end_date_time__gt=end).exists()
            outside       = Booking.objects.filter(location=location, start_date_time__gt=start, end_date_time__lt=end).exists()
            inside        = Booking.objects.filter(location=location, start_date_time__lt=start, end_date_time__gt=end).exists()

            if (overlap_start or overlap_end or inside or outside):
                self.add_error('location', "Occupied!")


class PoolResultForm(ModelForm):

    def __init__(self, *args,**kwargs):
        super (PoolResultForm,self ).__init__(*args,**kwargs)

    class Meta:
        model = PoolResult
        fields = ['winner', 'loser', 'balls_left']


    def clean(self):
        cleaned_data = super(PoolResultForm, self).clean()
        balls_left   = cleaned_data.get("balls_left")
        winner       = cleaned_data.get("winner")
        loser        = cleaned_data.get("loser")

        if (balls_left > 7):
            self.add_error('balls_left', "Aye?")

        if (winner == loser):
            self.add_error('winner', "Don't be a fud.")
            self.add_error('loser',  "Don't be a fud.")