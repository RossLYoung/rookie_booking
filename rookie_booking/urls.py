from django.conf import settings
from django.conf.urls import include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from .userprofile.urls import urlpatterns as userprofile_urls
from .dashboard.urls   import urlpatterns as dashboard_urls
from rookie_booking.booking_calendar.views import Index
from rookie_booking.booking_calendar.views import AddBooking, booking_events_api

urlpatterns = [
    url(r'^$',            Index.as_view(),    name='home'),
    url(r'^add-booking/$', AddBooking.as_view()),
    url(r'^api/bookings/$', booking_events_api, name='booking-events-api'),

    url(r'^dashboard/', include(dashboard_urls,    namespace='dashboard')),
    url(r'^profile/',   include(userprofile_urls,  namespace='userprofile')),
    url(r'^accounts/',  include('allauth.urls')),
    # url(r'^comments/',  include('django_comments.urls')),

    url(r'^backend/doc/', include('django.contrib.admindocs.urls')),
    url(r'^backend/',     include(admin.site.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +\
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]