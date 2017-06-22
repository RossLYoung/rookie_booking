from django.views.generic import ListView, TemplateView

class Index(TemplateView):
    template_name = 'booking_calendar/index.html'