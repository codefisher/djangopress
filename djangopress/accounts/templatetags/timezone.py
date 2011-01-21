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

@register.inclusion_tag('accounts/timezone.html')
def timezone(current):
    zone_names = {
        "Etc/GMT-8": "PST",
        "Etc/GMT-7": "MST",
        "Etc/GMT-6": "CST",
        "Etc/GMT-5": "EST",
        "Etc/GMT-4": "AST",
        "Etc/GMT-3": "ADT",
        "Etc/GMT":  "GMT",
        "Etc/GMT+1": "CET"
    }
    zones = [(("Etc/GMT", "00 GMT") if not i
                else ("Etc/GMT%+d" % i,
                      "%+03d %s" % (i, zone_names.get("Etc/GMT%+d" % i, ""))))
                for i in range(-12,13)]
    return {
        "zones": zones,
        "zone_names":zone_names,
        "current": current,
    }