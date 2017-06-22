from django.conf import settings


def get_setting_as_dict(name, short_name=None):
    short_name = short_name or name
    try:
        return {short_name: getattr(settings, name)}
    except AttributeError:
        return {}

# def mapbox_settings(request):
#     return {
#         'MAPBOX_API_KEY'    : settings.MAPBOX_API_KEY,
#         'MAPBOX_DEFAULT_MAP': settings.MAPBOX_DEFAULT_MAP
#     }