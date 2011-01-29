from django.conf import settings
from django import template
register = template.Library()

try:
    import pytz
except ImportError:
    pass # maybe notify that this could be installed?

@register.filter(name='user_timezone')
def user_timezone(value, arg):
    try:
        profile = arg.get_profile()
        zone = profile.timezone
        if not zone:
            zone = "Etc/GMT"
    except:
        zone = "Etc/GMT"
    try:
        tz = pytz.timezone(zone)
        c_tz = pytz.timezone(settings.TIME_ZONE)
        d_tz = c_tz.normalize(c_tz.localize(value))
        return d_tz.astimezone(tz)
    except:
        return value
