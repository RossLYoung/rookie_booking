from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import User



class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'first_name', 'last_name', 'username', 'is_staff', 'is_active', 'last_login')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields=('date_joined','last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'username', 'avatar_url')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        #(_('Ids'), {'fields': ('private_uuid', 'public_id')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2')}
    #     ),
    # )

admin.site.register(User, UserAdmin)

