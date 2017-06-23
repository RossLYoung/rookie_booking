import json

import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView, CreateView
from braces.views import LoginRequiredMixin

from rookie_booking.booking_calendar.forms import AddBookingForm, PoolResultForm
from rookie_booking.booking_calendar.models import Booking, Location, PoolResult


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'booking_calendar/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        return context


class AddBooking(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model           = Booking
    form_class      = AddBookingForm
    template_name   = "booking_calendar/_add_booking_modal.html"
    success_message = "Booked!"

    def get_context_data(self, **kwargs):
        context                       = super(AddBooking, self).get_context_data(**kwargs)
        context['submit_button_text'] = "Add"
        context['user_id']            = self.request.user.id
        return context

    def form_invalid(self, form):
        if self.request.is_ajax():
            message =  {"level_tag": 'error', "message": "Correct your errors!"}
            template = render_to_string(template_name=self.template_name,
                                        request=self.request,
                                        context={'form': form,
                                                 'submit_button_text': "Add",
                                                 'user_id':  self.request.user.id
                                                 })
            to_json = {'template':template, 'message': message, "result":False}
            return JsonResponse(json.dumps(to_json), safe=False)

    def form_valid(self, form):
         if self.request.is_ajax():

             form.fields['user'] = self.request.user
             self.object = form.save()

             event_json = {
                 "id"   : self.object.id,
                 "title": "{0} - {1}".format(self.object.user.username, self.object.description) ,
                 "start": self.object.start_date_time.isoformat(),
                 "end"  : self.object.end_date_time.isoformat(),
                 "color": self.object.location.color,
             }

             message = {"level_tag": 'success', "message": "Visit Updated!"}
             to_json = {'message': message, "result":True, "event": event_json}
             return JsonResponse(json.dumps(to_json), safe=False)

         return super(AddBooking, self).form_valid(form)


@login_required
def booking_events_api(request):

    utc=pytz.UTC
    if '-' in request.GET.get('start'):
        convert = lambda d: datetime.datetime.strptime(d, '%Y-%m-%d')
    else:
        convert = lambda d: datetime.datetime.utcfromtimestamp(float(d))
    start = utc.localize(convert(request.GET.get('start')))
    end   = utc.localize(convert(request.GET.get('end')))

    cache_name = "bookings" + str(start) + str(end)

    cached_result =  cache.get(cache_name)

    if not cached_result:

        response_data =[]

        bookings = Booking.objects.filter(start_date_time__gte=start, end_date_time__lte=end)

        for booking in bookings:

            response_data.append({
                "id": booking.id,
                "title": "{0} - {1}".format(booking.user.username, booking.description),
                "start": booking.start_date_time.astimezone(pytz.timezone('Europe/London')).isoformat(),
                "end":   booking.end_date_time.astimezone(pytz.timezone('Europe/London')).isoformat(),
                "color": booking.location.color,
            })

        results_json = json.dumps(response_data)
        cache.set(cache_name + str(start) + str(end),results_json, (60))
        return HttpResponse(results_json, content_type="application/json")

    return HttpResponse(cached_result,  content_type="application/json")


class PoolResults(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model           = PoolResult
    form_class      = PoolResultForm
    template_name   = "booking_calendar/pool.html"
    success_message = "Sorted!"

    def form_valid(self, form):
        form.fields['created_by'] = self.request.user
        self.object = form.save()

