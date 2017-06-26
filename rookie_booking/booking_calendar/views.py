import json

import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from braces.views import LoginRequiredMixin

from rookie_booking.booking_calendar.forms import AddBookingForm, PoolResultForm
from rookie_booking.booking_calendar.models import Booking, Location, PoolResult
from rookie_booking.userprofile.models import User


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

    # cache_name = "bookings" + str(start) + str(end)

    # cached_result =  cache.get(cache_name)

    # if not cached_result:

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
    # cache.set(cache_name + str(start) + str(end),results_json, (60))
    return HttpResponse(results_json, content_type="application/json")

    # return HttpResponse(cached_result,  content_type="application/json")


from django.utils import timezone

from dateutil.relativedelta import relativedelta, MO


class PoolResults(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model           = PoolResult
    form_class      = PoolResultForm
    template_name   = "booking_calendar/pool.html"
    success_message = "Sorted!"
    success_url     = reverse_lazy('booking:pool')

    def get_context_data(self, **kwargs):
        context = super(PoolResults, self).get_context_data(**kwargs)
        context['results'] = PoolResult.objects.all().order_by('-created_on')

        now            = timezone.datetime.now()
        start_of_week  = now.replace(hour=0, minute=0, second=0) + relativedelta(weekday=MO(-1))
        start_of_month = now.replace(day=1)
        start_of_year  = now.replace(month=1, day=1)

        stats = {}

        for user in User.objects.all():
            stats[user.username] = {
                'total_week'   : 0,
                'total_month'  : 0,
                'total_year'   : 0,
                'wins_week'    : 0,
                'wins_month'   : 0,
                'wins_year'    : 0,
                'losses_week'  : 0,
                'losses_month' : 0,
                'losses_year'  : 0,
                'ratio_week'   : 0,
                'ratio_month'  : 0,
                'ratio_year'   : 0,
            }

        def percent(wins, total):
            if total == 0:
                return 0
            return (wins / total) * 100



        for result in PoolResult.objects.filter(created_on__gte=start_of_week):
            stats[result.winner.username]['total_week'] += 1
            stats[result.winner.username]['wins_week']  += 1
            stats[result.loser.username]['total_week']  += 1
            stats[result.loser.username]['losses_week'] += 1

        for result in PoolResult.objects.filter(created_on__gte=start_of_month):
            stats[result.winner.username]['total_month'] += 1
            stats[result.winner.username]['wins_month']  += 1
            stats[result.loser.username]['total_month']  += 1
            stats[result.loser.username]['losses_month'] += 1

        for result in PoolResult.objects.filter(created_on__gte=start_of_year):
            stats[result.winner.username]['total_year'] += 1
            stats[result.winner.username]['wins_year']  += 1
            stats[result.loser.username]['total_year']  += 1
            stats[result.loser.username]['losses_year'] += 1


        for user in stats:
            stats[user]['ratio_week']  = percent(float(stats[user]['wins_week'])  , float(stats[user]['total_week']))
            stats[user]['ratio_month'] = percent(float(stats[user]['wins_month']) , float(stats[user]['total_month']))
            stats[user]['ratio_year']  = percent(float(stats[user]['wins_year'])  , float(stats[user]['total_year']))

        context['stats'] = stats


        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # form.fields['created_by'] = self.request.user.id
        self.object = form.save()

        return super(PoolResults, self).form_valid(form)

