from django.contrib import admin
from .models import PoolResult, SpeedRun


class PoolResultAdmin(admin.ModelAdmin):
    list_display = ('winner', 'loser', 'created_on')
    ordering = ('-created_on',)


class PoolSpeedRunAdmin(admin.ModelAdmin):
    list_display = ('person','verified_by', 'time', 'created_on')
    ordering = ('-time',)

admin.site.register(PoolResult, PoolResultAdmin)
admin.site.register(SpeedRun, PoolSpeedRunAdmin)