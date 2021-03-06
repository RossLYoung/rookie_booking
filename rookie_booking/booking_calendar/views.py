import json
import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from braces.views import LoginRequiredMixin
from django.utils import timezone

from dateutil.relativedelta import relativedelta, MO

from rookie_booking.booking_calendar.forms import AddBookingForm, PoolResultForm, EditBookingForm, PoolSpeedRunForm
from rookie_booking.booking_calendar.models import Booking, Location, PoolResult, SpeedRun
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
            message  = {"level_tag": 'error', "message": "Correct your errors!"}
            template = render_to_string(template_name=self.template_name,
                                        request=self.request,
                                        context={'form': form,
                                                 'submit_button_text': "Add",
                                                 'user_id':  self.request.user.id
                                                 })
            to_json = {'template': template, 'message': message, "result": False}
            return JsonResponse(json.dumps(to_json), safe=False)

    def form_valid(self, form):
        if self.request.is_ajax():
            form.fields['user'] = self.request.user
            self.object = form.save()
            event_json = {
                "id"   : self.object.id,
                "user_id": self.object.user.id,
                "title": "{0} - {1}".format(self.object.user.username.encode('utf-8'), self.object.description) ,
                "start": self.object.start_date_time.isoformat(),
                "end"  : self.object.end_date_time.isoformat(),
                "color": self.object.location.color,
            }
            message = {"level_tag": 'success', "message": "Booking Created!"}
            to_json = {'message': message, "result": True, "event": event_json}
            return JsonResponse(json.dumps(to_json), safe=False)
        return super(AddBooking, self).form_valid(form)


class EditBooking(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model           = Booking
    form_class      = EditBookingForm
    template_name   = "booking_calendar/_edit_booking_modal.html"
    success_message = "Updated!"
    pk_url_kwarg    = 'booking_id'

    def get_context_data(self, **kwargs):
        context                       = super(EditBooking, self).get_context_data(**kwargs)
        context['submit_button_text'] = "Update"
        return context

    def form_invalid(self, form):
        if self.request.is_ajax():
            message  = {"level_tag": 'error', "message": "Correct your errors!"}
            template = render_to_string(template_name=self.template_name,
                                        request=self.request,
                                        context={'form': form,
                                                 'submit_button_text': "Update",
                                                 'user_id':  self.request.user.id
                                                 })
            to_json = {'template': template, 'message': message, "result": False}
            return JsonResponse(json.dumps(to_json), safe=False)

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            event_json  = {
                "id"     : self.object.id,
                "user_id": self.object.user.id,
                "title"  : "{0} - {1}".format(self.object.user.username.encode('utf-8'), self.object.description) ,
                "start"  : self.object.start_date_time.isoformat(),
                "end"    : self.object.end_date_time.isoformat(),
                "color"  : self.object.location.color,
            }
            message = {"level_tag": 'success', "message": "Booking Updated!"}
            to_json = {'message': message, "result": True, "event": event_json}
            return JsonResponse(json.dumps(to_json), safe=False)
        return super(EditBooking, self).form_valid(form)










@login_required
def remove_booking_event(request, booking_id):
    if request.method == 'POST':
        if request.is_ajax():
            booking = Booking.objects.get(pk=booking_id)
            if request.user == booking.user:
                booking.delete()
                message = {"level_tag": 'success', "message": "Booking Deleted!"}
                to_json = {'message': message, "result": True, "booking_id": booking_id}
            else:
                message = {"level_tag": 'error', "message": "Not allowed!"}
                to_json = {'message': message, "result": False, "booking_id": booking_id}
            return JsonResponse(json.dumps(to_json), safe=False)

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

    response_data = []

    bookings = Booking.objects.filter(start_date_time__gte=start, end_date_time__lte=end)

    for booking in bookings:

        response_data.append({
            "id": booking.id,
            "user_id": booking.user.id,
            "title": "{0} - {1}".format(booking.user.username.encode('utf-8'), booking.description.encode('utf-8')),
            "start": booking.start_date_time.astimezone(pytz.timezone('Europe/London')).isoformat(),
            "end":   booking.end_date_time.astimezone(pytz.timezone('Europe/London')).isoformat(),
            "color": booking.location.color,
        })

    results_json = json.dumps(response_data)
    # cache.set(cache_name + str(start) + str(end),results_json, (60))
    return HttpResponse(results_json, content_type="application/json")

    # return HttpResponse(cached_result,  content_type="application/json")


def percent(wins, total):
    if total == 0:
        return 0
    return (wins / total) * 100

def get_kfactor(elo_rating):
    if elo_rating <= 2100:
        return 32.0
    elif elo_rating > 2100 and elo_rating <= 2400:
        return 24.0
    else:
        return 16.0

def calculate_elo(winner_elo, loser_elo):
    # Calculate winner elo
    winner_odds = 1.0 / (1.0 + pow(10.0, (loser_elo - winner_elo) / 400.0))
    new_winner_elo = round(winner_elo + (get_kfactor(winner_elo) * (1.0 - winner_odds)))

    loser_odds = 1.0 / (1.0 + pow(10.0, (winner_elo - loser_elo) / 400.0))
    new_loser_elo = round(loser_elo + (get_kfactor(loser_elo) * (0.0 - loser_odds)))

    return (new_winner_elo, new_loser_elo)

granny_descriptions = [
    "was absolutely pumped by",
    "was worn like a sock puppet by",
    "has been turned inside-out by",
    "was humiliated by",
    "needs to re-evaluate everything because of",
    "was thoroughly bested by",
    "is not worthy to lick the boots of",
    "should probably seek counselling because of",
    "\"should have gone to specsavers\", says"
]

def get_user_stats():
    # make a dict of dicts with the following shape for each user
    # total not implemented - will need to add an all-time count for when we enter a new year
    stats = {}
    for user in User.objects.all():
        stats[user.username] = {
            'hide_from_stats': user.hide_from_stats,

            'total_week': 0,
            'total_month': 0,
            'total_year': 0,

            'wins_week': 0,
            'wins_month': 0,
            'wins_year': 0,
            'losses_week': 0,
            'losses_month': 0,
            'losses_year': 0,

            'ratio_week': 0,
            'ratio_month': 0,
            'ratio_year': 0,

            'elo': 1200,
        }

    now = timezone.datetime.now()
    start_of_week = now.replace(hour=0, minute=0, second=0) + relativedelta(weekday=MO(-1))
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0)
    start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0)

    # for the last week, month, and year, sum the wins and losses for each user
    for result in PoolResult.objects.filter(created_on__gte=start_of_week).select_related('winner', 'loser'):
        stats[result.winner.username]['total_week'] += 1
        stats[result.winner.username]['wins_week'] += 1
        stats[result.loser.username]['total_week'] += 1
        stats[result.loser.username]['losses_week'] += 1

    for result in PoolResult.objects.filter(created_on__gte=start_of_month).select_related('winner', 'loser'):
        stats[result.winner.username]['total_month'] += 1
        stats[result.winner.username]['wins_month'] += 1
        stats[result.loser.username]['total_month'] += 1
        stats[result.loser.username]['losses_month'] += 1

    for result in PoolResult.objects.filter(created_on__gte=start_of_year).select_related('winner', 'loser'):
        stats[result.winner.username]['total_year'] += 1
        stats[result.winner.username]['wins_year'] += 1
        stats[result.loser.username]['total_year'] += 1
        stats[result.loser.username]['losses_year'] += 1

    # then get the weekly, monthly, and yearly win percentage
    for user in stats:
        stats[user]['ratio_week'] = percent(float(stats[user]['wins_week']), float(stats[user]['total_week']))
        stats[user]['ratio_month'] = percent(float(stats[user]['wins_month']), float(stats[user]['total_month']))
        stats[user]['ratio_year'] = percent(float(stats[user]['wins_year']), float(stats[user]['total_year']))

    return stats

def get_elo_diffs(stats):
    diffs = []
    for result in PoolResult.objects.all().order_by('created_on').select_related('winner', 'loser'):
        winner_elo = stats[result.winner.username]['elo']
        loser_elo = stats[result.loser.username]['elo']

        new_winner_elo, new_loser_elo = calculate_elo(winner_elo, loser_elo)

        stats[result.winner.username]['elo'] = new_winner_elo
        stats[result.loser.username]['elo']  = new_loser_elo

        winner_diff = new_winner_elo - winner_elo
        loser_diff  = new_loser_elo  - loser_elo

        diffs.append({
            'winner_elo'      : winner_diff,
            'loser_elo'       : loser_diff,
            'winner_elo_total': new_winner_elo,
            'loser_elo_total' : new_loser_elo
        })

    return reversed(diffs)


class PoolResults(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model           = PoolResult
    form_class      = PoolResultForm
    template_name   = "booking_calendar/pool.html"
    success_message = "Sorted!"
    success_url     = reverse_lazy('booking:pool')

    def get_context_data(self, **kwargs):
        context = super(PoolResults, self).get_context_data(**kwargs)

        # anyone been pumped today?
        context['todays_grannies']     = PoolResult.objects.filter(created_on__date=datetime.date.today(), balls_left=7)
        context['granny_descriptions'] = granny_descriptions

        stats = get_user_stats()

        diffs = get_elo_diffs(stats)

        results = PoolResult.objects.order_by('-created_on').select_related('winner', 'loser')
        context['zippedResults'] = zip(results, diffs)
        context['stats'] = stats

        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        return super(PoolResults, self).form_valid(form)


# from django.core.cache import cache

@login_required
def pool_result_json(request):
    stats         = get_user_stats()
    diffs         = get_elo_diffs(stats)
    results       = PoolResult.objects.order_by('-created_on').select_related('winner', 'loser')
    zippedResults = zip(results, diffs)

    response_data ={
        "currentUser": request.user.username,
        "data": []
    }

    for result, elo_stuff in zippedResults:
        response_data["data"].append({
            "id"              : result.id,
            "date"            : result.created_on.strftime('%s') + "###" + result.created_on.strftime('%a, %d %b, %H:%M'),
            "day"             : result.created_on.weekday(),
            "winner"          : result.winner.username,
            "loser"           : result.loser.username,
            "elo"             : elo_stuff["winner_elo"],  # can be winner or loser as they're the same
            "winner_elo_total": elo_stuff["winner_elo_total"],
            "loser_elo_total" : elo_stuff["loser_elo_total"],
            "balls_left"      : result.balls_left
        })

    # results_json = json.dumps({"results": response_data})

    # cache.set("acall-" + query_string, results_json, 60)
    return JsonResponse(response_data, safe=False)
    # return JsonResponse(cached_result, safe=False)

class PoolStats(LoginRequiredMixin, TemplateView):
    template_name = 'booking_calendar/stats.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PoolStats, self).get_context_data(**kwargs)
    #     return context

class PoolSpeedRun(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model           = SpeedRun
    form_class      = PoolSpeedRunForm
    template_name   = "booking_calendar/speedrun.html"
    success_message = "Sorted!"
    success_url     = reverse_lazy('booking:pool-timed')

    def get_context_data(self, **kwargs):
        context = super(PoolSpeedRun, self).get_context_data(**kwargs)
        results = SpeedRun.objects.order_by('-time').select_related('person', 'verified_by')
        context['speedruns'] = results
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        return super(PoolSpeedRun, self).form_valid(form)

