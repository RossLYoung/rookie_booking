from django.conf.urls import url

from .views import AddBooking, EditBooking, booking_events_api, PoolResults, remove_booking_event

urlpatterns = [
    url(r'^add-booking/$',  AddBooking.as_view()),
    url(r'^edit-booking/(?P<booking_id>[0-9]+)/$', EditBooking.as_view()),
    url(r'^api/bookings/$', booking_events_api,    name='booking-events-api'),
    url(r'^pool/$',         PoolResults.as_view(), name='pool'),
    url(r'^removebooking/(?P<booking_id>[0-9]+)/$', remove_booking_event, name='remove-booking'),

]
