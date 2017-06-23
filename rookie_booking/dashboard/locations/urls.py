from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',               views.DashLocationList.as_view(),   name='locations'),

    # url(r'^(?P<pk>[0-9]+)$',         views.DashLevelUpdate.as_view(), name='level'),
    # url(r'^add/$',                   views.DashLevelCreate.as_view(), name='level-add'),
    # url(r'^(?P<pk>[0-9]+)/delete/$', views.DashLevelDelete.as_view(), name='level-delete'),
]
