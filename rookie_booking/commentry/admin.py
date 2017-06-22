from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from models import MPTTComment

admin.site.register(MPTTComment, DjangoMpttAdmin)
