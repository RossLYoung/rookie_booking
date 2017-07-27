from django.contrib import admin
from .models import PoolResult

class PoolResultAdmin(admin.ModelAdmin):
    list_display = ('winner', 'loser', 'created_on')
    ordering = ('-created_on',)

admin.site.register(PoolResult, PoolResultAdmin)