from __future__ import unicode_literals
import re
import hashlib

from django.conf import settings
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import user_signed_up

from .countries import COUNTRY_CHOICES

class UserManager(BaseUserManager):

    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})
        try:
            return self.get_query_set().get(**kwargs), False
        except self.model.DoesNotExist:
            defaults.update(kwargs)
            return self.create_user(**defaults), True

    def create_user(self, email, password=None, is_staff=False, is_active=True, **extra_fields):
        'Creates a User with the given username, email and password'
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):

    email       = models.EmailField(unique=True)
    first_name  = models.CharField(_('first name'), max_length=40, blank=True, null=True,  unique=False)
    last_name   = models.CharField(_('last name'),  max_length=40, blank=True, null=True,  unique=False)
    username    = models.CharField(_('user name'),  max_length=40, blank=False, null=False, unique=True, default="")
    is_staff    = models.BooleanField(pgettext_lazy('User field', 'staff status'), default=False)
    is_active   = models.BooleanField(pgettext_lazy('User field', 'active'), default=False)
    date_joined = models.DateTimeField(pgettext_lazy('User field', 'date joined'), default=timezone.now, editable=False)
    avatar_url = models.CharField(max_length=256, blank=True, null=True, default='/static/img/userprofile/default-avatar.svg')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD    = 'email'

    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        app_label = 'userprofile'

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_username(self):
        'Return the identifying username for this User'
        return self.username


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=['password'])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def guess_display_name(self):
        """Set a display name, if one isn't already set."""
        if self.username:
            return

        if self.first_name and self.last_name:
            un = "%s %s" % (self.first_name, self.last_name[0]) # like "Andrew E"
        elif self.first_name:
            un = self.first_name
        else:
            un = 'You'
        self.username = un.strip()


@receiver(user_signed_up)
def set_initial_user_names(request, user, sociallogin=None, **kwargs):
    """
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    """

    preferred_avatar_size_pixels=256

    picture_url = "http://www.gravatar.com/avatar/{0}?s={1}".format(
        hashlib.md5(user.email.encode('UTF-8')).hexdigest(),
        preferred_avatar_size_pixels
    )

    verified = False

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            user.first_name = name.split()[0]
            try:
                user.last_name  = name.split()[1]
            except:
                pass
            user.username   = sociallogin.account.extra_data['screen_name']
            verified        = sociallogin.account.extra_data['verified']
            verified        = True
            picture_url     =  sociallogin.account.get_avatar_url()

        if sociallogin.account.provider == 'facebook':
            user.first_name = sociallogin.account.extra_data['first_name']
            user.last_name  = sociallogin.account.extra_data['last_name']
            user.username   = sociallogin.account.extra_data['name']
            verified        = sociallogin.account.extra_data['verified']
            picture_url     = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
                sociallogin.account.uid, preferred_avatar_size_pixels)

        if sociallogin.account.provider == 'google':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name  = sociallogin.account.extra_data['family_name']
            #verified       = sociallogin.account.extra_data['verified_email']
            picture_url     = sociallogin.account.extra_data['picture']

        if sociallogin.account.provider == 'slack':
            user.first_name = sociallogin.account.extra_data['given_name']
            user.last_name  = sociallogin.account.extra_data['family_name']
            #verified       = sociallogin.account.extra_data['verified_email']
            picture_url     = sociallogin.account.extra_data['picture']



        if verified:
            user.is_active = True

    user.is_active = True
    user.avatar_url = picture_url
    user.guess_display_name()
    user.save()