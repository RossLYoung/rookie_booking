
from django.contrib.messages.views import SuccessMessageMixin
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from extra_views import ModelFormSetView

from rookie_booking.booking_calendar.models import Location


class DashLocationList(StaffuserRequiredMixin, SuccessMessageMixin, ModelFormSetView):
    context_object_name = 'locations'
    template_name = 'dashboard/locations/location_list.html'
    model = Location
    extra = 1
    success_message = "Locations Updated!"
    fields = ('name', 'description','color')
