from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',              views.profile_details,      name='profile-details'),
    url(r'^email/$',        views.profile_email,        name='profile-email'),
    url(r'^password/$',     views.profile_passsword,    name='profile-password'),
    url(r'^password/set/$', views.profile_password_set, name='profile-password-set'),
    url(r'^social/$',       views.profile_social,       name='profile-social'),
]
