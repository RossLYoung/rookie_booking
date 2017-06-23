from django.conf.urls import url

from .views import AddBooking, booking_events_api, PoolResults

urlpatterns = [
    url(r'^add-booking/$',  AddBooking.as_view()),
    url(r'^api/bookings/$', booking_events_api,    name='booking-events-api'),
    url(r'^pool/$',         PoolResults.as_view(), name='pool'),
]
