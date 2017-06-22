from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required \
    as _staff_member_required

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from braces.views import StaffuserRequiredMixin


class DashHome(StaffuserRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'




def staff_member_required(f):
    return _staff_member_required(f, login_url='account_login')


class StaffMemberOnlyMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffMemberOnlyMixin, self).dispatch(*args, **kwargs)




