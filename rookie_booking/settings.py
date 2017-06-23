# -*- coding: utf-8 -*-

import os
import sys
from os.path import join, dirname, basename, abspath

from configurations import Configuration, values

from .config.fab_settings import  * #need Static/Media dirs as they differ between dev&prod

try:
    from S3 import CallingFormat
    AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
except ImportError:
    # TODO: Fix this where even if in Dev this class is called.
    pass

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(__file__)

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'rookie_booking'))
sys.path.insert(0, PROJECT_DIR)


class Common(Configuration):

    DEBUG = values.BooleanValue(True)

    SECRET_KEY = values.SecretValue()

    FIXTURE_DIRS = (join(BASE_DIR, 'fixtures'),)

    ADMINS = (
        ('Ross', 'ross@rosslyoung.com'),
    )

    MANAGERS = ADMINS

    TIME_ZONE = 'Europe/London'

    LANGUAGE_CODE = 'en-gb'

    SITE_ID = 1

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    DATABASES = values.DatabaseURLValue(environ_name='DATABASE_URL_LOCAL')

    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
        }
    }

    DJANGO_APPS = [
        #'django_admin_bootstrapped.bootstrap3',
        'django_admin_bootstrapped',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.admindocs',
        'django.contrib.gis',
    ]

    LOCAL_APPS = [
        'rookie_booking.booking_calendar',
        'rookie_booking.userprofile',
        # 'rookie_booking.commentry',
        'rookie_booking.core',
        'rookie_booking.dashboard',
    ]

    THIRD_PARTY_APPS = [
        # 'django_comments',
        'bootstrap3',
        'widget_tweaks',
        'gunicorn',
        'configurations',
        'mptt',
        'django_mptt_admin',
        'crispy_forms',

        'versatileimagefield',
        'materializecssform',

        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.twitter',
        'allauth.socialaccount.providers.google',
    ]

    INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

    COMMENTS_APP = 'rookie_booking.commentry'

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    TEMPLATES = [

        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'rookie_booking', 'commentry', 'templates'),
                os.path.join(BASE_DIR, 'templates', 'allauth'),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                ],
                'debug':  DEBUG,
                'string_if_invalid':  "<< MISSING VARIABLE >>",
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
            },
        },
    ]

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "rookie_booking", "static"),
        os.path.join(BASE_DIR, "rookie_booking", "commentry", "static"),
    )

    STATIC_ROOT = join(BASE_DIR,'static_site_wide')

    MEDIA_ROOT = join(PROJECT_DIR,'media')

    MEDIA_URL = '/media/'

    ROOT_URLCONF = 'rookie_booking.urls'

    WSGI_APPLICATION = 'rookie_booking.wsgi.application'

    LOGIN_URL = '/accounts/login/'

    LOGIN_REDIRECT_URL = 'home' #named url

    AUTH_USER_MODEL = 'userprofile.User'

    AUTHENTICATION_BACKENDS = (
         "django.contrib.auth.backends.ModelBackend",
         "allauth.account.auth_backends.AuthenticationBackend",
    )

    # ACCOUNT_ADAPTER = "userprofile.adapter.UserProfileAccountAdapter"
    ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"
    ACCOUNT_AUTHENTICATION_METHOD ="email"
    ACCOUNT_CONFIRM_EMAIL_ON_GET =True
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = LOGIN_URL
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL =None
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
    ACCOUNT_EMAIL_REQUIRED =True
    ACCOUNT_EMAIL_VERIFICATION ="mandatory"
    ACCOUNT_EMAIL_SUBJECT_PREFIX ="[Site]"
    ACCOUNT_DEFAULT_HTTP_PROTOCOL ="http"
    ACCOUNT_FORMS ={}
    ACCOUNT_LOGOUT_ON_GET =False
    ACCOUNT_LOGOUT_REDIRECT_URL ="/"
    ACCOUNT_SIGNUP_FORM_CLASS =None
    ACCOUNT_SIGNUP_PASSWORD_VERIFICATION =True
    ACCOUNT_UNIQUE_EMAIL =True
    ACCOUNT_USER_MODEL_USERNAME_FIELD ="username"
    ACCOUNT_USER_MODEL_EMAIL_FIELD ="email"
    #ACCOUNT_USER_DISPLAY =a callable returning user.username
    ACCOUNT_USERNAME_MIN_LENGTH =1
    ACCOUNT_USERNAME_BLACKLIST =[]
    ACCOUNT_USERNAME_REQUIRED =True
    ACCOUNT_PASSWORD_INPUT_RENDER_VALUE =False
    ACCOUNT_PASSWORD_MIN_LENGTH =6
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
    ACCOUNT_SESSION_REMEMBER =None
    ACCOUNT_SESSION_COOKIE_AGE =1814400
    SOCIALACCOUNT_ADAPTER ="userprofile.adapter.UserProfileSocialAccountAdapter"
    #SOCIALACCOUNT_ADAPTER ="allauth.socialaccount.adapter.DefaultSocialAccountAdapter"
    SOCIALACCOUNT_QUERY_EMAIL =ACCOUNT_EMAIL_REQUIRED
    SOCIALACCOUNT_AUTO_SIGNUP =True
    SOCIALACCOUNT_EMAIL_REQUIRED =ACCOUNT_EMAIL_REQUIRED ############
    SOCIALACCOUNT_EMAIL_VERIFICATION ='optional' #################
    SOCIALACCOUNT_FORMS ={}
    SOCIALACCOUNT_PROVIDERS = dict
    SOCIALACCOUNT_STORE_TOKENS =True

    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"


class Development(Common):
    # DEBUG = values.BooleanValue(False)
    ALLOWED_HOSTS = ["127.0.0.1", "192.168.1.19", "192.168.101.237"]

    INSTALLED_APPS = Common.INSTALLED_APPS

    DEFAULT_FROM_EMAIL   = values.Value('Rookie Booking Admin <ross@rosslyoung.com>')
    EMAIL_HOST    = "localhost"
    EMAIL_PORT    = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')

    ######################################################################
    ########## DJANGO DEBUG TOOLBAR CONFIGURATION ########################
    ######################################################################

    MIDDLEWARE = Common.MIDDLEWARE + ['debug_toolbar.middleware.DebugToolbarMiddleware',
                                                      # 'django.contrib.admindocs.middleware.XViewMiddleware',
                                                      # 'debugtools.middleware.XViewMiddleware',
    ]

    INSTALLED_APPS += [
                        # 'debug_toolbar',
                       # 'template_timings_panel',
                       # 'template_profiler_panel',
                       # 'debugtools',
    ]

    INTERNAL_IPS = ['127.0.0.1', 'localhost','app1', '192.168.11.1', '192.168.1.101']


    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }

    DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',

    #3rd party
    # 'template_profiler_panel.panels.template.TemplateProfilerPanel',
    # 'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

    # DISABLE_PANELS = set(['debug_toolbar.panels.redirects.RedirectsPanel'])

    ########## end django-debug-toolbar


class Production(Common):

    DEBUG = values.BooleanValue(False)

    DATABASES = values.DatabaseURLValue(environ_name='DATABASE_URL')

    INSTALLED_APPS = Common.INSTALLED_APPS

    SECRET_KEY = values.SecretValue()

    STATIC_ROOT = STATIC_DIR

    MEDIA_ROOT  = MEDIA_DIR

    ALLOWED_HOSTS = ["rookie-booking.rosslyoung.com"]

    ######################################################################
    ########## STORAGE CONFIGURATION #####################################
    ######################################################################

    # # See: http://django-storages.readthedocs.org/en/latest/index.html
    # INSTALLED_APPS += (
    #     'storages',
    # )
    #
    # # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    # STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    #
    # # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    # AWS_ACCESS_KEY_ID       = values.SecretValue()
    # AWS_SECRET_ACCESS_KEY   = values.SecretValue()
    # AWS_STORAGE_BUCKET_NAME = values.SecretValue()
    # AWS_AUTO_CREATE_BUCKET  = True
    # AWS_QUERYSTRING_AUTH    = False
    #
    # # see: https://github.com/antonagestam/collectfast
    # AWS_PRELOAD_METADATA = True
    # INSTALLED_APPS += ("collectfast", )
    #
    # # AWS cache settings, don't change unless you know what you're doing:
    # AWS_EXPIREY = 60 * 60 * 24 * 7
    # AWS_HEADERS = {
    #     'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
    #         AWS_EXPIREY)
    # }
    #
    # # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    # STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    # ########## END STORAGE CONFIGURATION
    #

    EMAIL_BACKEND     = "sgbackend.SendGridBackend"
    SENDGRID_API_KEY  = values.SecretValue(environ_prefix="", environ_name="SENDGRID_API_KEY")

    DEFAULT_FROM_EMAIL   = values.Value('Rookie Booking Admin <ross@rosslyoung.com>')

    TEMPLATES = [

        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'rookie_booking', 'commentry', 'templates'),
                os.path.join(BASE_DIR, 'templates', 'allauth'),
            ],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                ],
                'debug':  DEBUG,
                'string_if_invalid':  "",
                'loaders': [
                    ('django.template.loaders.cached.Loader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            },
        },
    ]

    SESSION_CACHE_ALIAS = "default"
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://cache-private:6383/0",
            "OPTIONS": {
                #"CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PARSER_CLASS": "redis.connection.HiredisParser",
            }
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/www/logs/rookie_booking/application.log',
            },
        },
        'loggers': {
            'loggyMcLog': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.template': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


