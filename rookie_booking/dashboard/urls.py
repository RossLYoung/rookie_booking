from django.conf.urls import url, include

from .locations.urls import urlpatterns as location_urls

from .views import DashHome

urlpatterns = [
    url(r'^$', DashHome.as_view(), name='index'),
    url(r'^locations/',        include(location_urls)),
]
