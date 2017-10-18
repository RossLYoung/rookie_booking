from django.conf.urls import url

from .views import AddBooking, EditBooking, booking_events_api, PoolResults, remove_booking_event, PoolSpeedRun, pool_result_json, PoolStats

urlpatterns = [
    url(r'^add-booking/$',  AddBooking.as_view()),
    url(r'^edit-booking/(?P<booking_id>[0-9]+)/$', EditBooking.as_view()),
    url(r'^api/bookings/$', booking_events_api,                           name='booking-events-api'),
    url(r'^pool/$',         PoolResults.as_view(),                        name='pool'),
    url(r'^api/pool-results/$', pool_result_json,                         name='pool-api'),
    url(r'^pool-stats/$',   PoolStats.as_view(),                          name='pool-stats'),

    url(r'^pool-speedrun/$', PoolSpeedRun.as_view(),                      name='pool-timed'),

    url(r'^removebooking/(?P<booking_id>[0-9]+)/$', remove_booking_event, name='remove-booking'),

]
