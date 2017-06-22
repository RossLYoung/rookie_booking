from django.views.generic import ListView, TemplateView
from braces.views import LoginRequiredMixin

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'booking_calendar/index.html'