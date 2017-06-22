from django.conf.urls import url, include

from .views import DashHome

urlpatterns = [
    url(r'^$', DashHome.as_view(), name='index'),

]
