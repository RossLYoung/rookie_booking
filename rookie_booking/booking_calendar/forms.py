from django.forms import ModelForm

from rookie_booking.booking_calendar.models import Booking
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

            overlap_start = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gte=start).exists()
            overlap_end   = Booking.objects.filter(location=location, start_date_time__lte=end,   end_date_time__gte=end).exists()
            outside       = Booking.objects.filter(location=location, start_date_time__gte=start, end_date_time__lte=end).exists()
            inside        = Booking.objects.filter(location=location, start_date_time__lte=start, end_date_time__gte=end).exists()

            if (overlap_start or overlap_end or inside or outside):
                self.add_error('location', "Occupied!")