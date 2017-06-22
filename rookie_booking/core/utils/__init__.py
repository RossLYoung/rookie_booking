# coding: utf-8
from __future__ import unicode_literals

import re

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
# from django.http.request import absolute_http_url_re
from django.template.response import TemplateResponse
from django.utils.encoding import iri_to_uri, smart_text
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


__all__ = ['build_absolute_uri']

absolute_http_url_re = re.compile(r"^https?://", re.I)



def build_absolute_uri(location, is_secure=False):
    try:
        host = settings.CANONICAL_HOSTNAME
    except AttributeError:
        raise ImproperlyConfigured('You need to specify CANONICAL_HOSTNAME in '
                                   'your Django settings file')
    if not absolute_http_url_re.match(location):
        current_uri = '%s://%s' % ('https' if is_secure else 'http', host)
        location = urljoin(current_uri, location)
    return iri_to_uri(location)
