from django.conf import settings
from django import forms

from widgets_datetime import DateWidget, TimeWidget, DateTimeWidget

dateOptions = {
    'format': 'dd/mm/yyyy',
    'autoclose': True,
    'showMeridian' : True,
    'todayHighlight': True,
    'clearBtn': False
}

dateTimeOptions = {
    'format': 'dd/mm/yyyy hh:ii',
    'autoclose': True,
    'showMeridian' : True,
    'todayHighlight': True,
    'clearBtn': False
}

dateAttrs = {
    'readonly': ''
}

timeOptions = {
    'format': 'hh:ii',
    'autoclose': True,
    'showMeridian' : True,
    'clearBtn': False
}


class CustomDatePicker(DateWidget):
    glyphicon = 'glyphicon-booking_calendar fa fa-booking_calendar' #annoyingly needs the glyphicon class

    def _media(self):
        datepicker = settings.STATIC_URL + 'js/bootstrap-datetimepicker.js'
        return forms.Media(js=(datepicker,),
                           css={'all': ('css/datetimepicker.css',)},)

    media = property(_media)

    def __init__(self, attrs=None, options=None, usel10n=None, bootstrap_version=None):
        if options is None:
            options = {}
        options['format'] = options.get('format', 'dd/mm/yyyy hh:ii')
        super(CustomDatePicker, self).__init__(attrs, options, usel10n, bootstrap_version)


class CustomDateTimePicker(DateTimeWidget):
    glyphicon = 'glyphicon-booking_calendar fa fa-calendar' #annoyingly needs the glyphicon class

    def _media(self):
        datepicker = settings.STATIC_URL + 'js/bootstrap-datetimepicker.js'
        return forms.Media(js=(datepicker,),
                           css={'all': ('css/datetimepicker.css',)},)

    media = property(_media)

    def __init__(self, attrs=None, options=None, usel10n=None, bootstrap_version=None):
        if options is None:
            options = {}
        options['format'] = options.get('format', 'dd/mm/yyyy hh:ii')
        super(CustomDateTimePicker, self).__init__(attrs, options, usel10n, bootstrap_version)


class CustomTimePicker(TimeWidget):
    glyphicon = 'glyphicon-booking_calendar fa fa-clock-o' #annoyingly needs the glyphicon class

    def _media(self):
        datepicker = settings.STATIC_URL + 'js/bootstrap-datetimepicker.js'
        return forms.Media(js=(datepicker,),
                           css={'all': ('css/datetimepicker.css',)},)

    media = property(_media)

    def __init__(self, attrs=None, options=None, usel10n=None, bootstrap_version=None):
        if options is None:
            options = {}
        # Set the default options to show only the timepicker object
        options['startView'] = options.get('startView', 1)
        options['minView']   = options.get('minView', 0)
        options['maxView']   = options.get('maxView', 1)
        options['format']    = options.get('format', 'hh:ii')
        super(CustomTimePicker, self).__init__(attrs, options, usel10n, bootstrap_version)
