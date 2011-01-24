import collections
import pytz
from django import forms

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
short_zones = []
for i in range(-12,13):
    if not i:
        short_zones.append(("Etc/GMT", "GMT"))
    else:
        name = zone_names.get("Etc/GMT%+d" % i, "")
        if name:
            short_zones.append(("Etc/GMT%+d" % i, "GMT %+03d (%s)" % (i, name)))
        else:
            short_zones.append(("Etc/GMT%+d" % i, "GMT %+03d" % i))

zones = collections.defaultdict(list)
for zone in pytz.common_timezones:
    region, _, city = zone.partition("/")
    if region != "GMT":
        zones[region].append((zone, zone.replace("_", " ").replace("/", " - ")))
long_zones = sorted([(region, list(sorted(items)))
                        for region, items in zones.items()
                    ] + [("GMT", short_zones)])

class TimeZoneField(forms.ChoiceField):
    def __init__(self, simple_zones=True, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        if simple_zones:
            super(TimeZoneField, self).__init__(short_zones, required,
                        widget, label, initial, help_text, *args, **kwargs)
        else:
            super(TimeZoneField, self).__init__(long_zones, required,
                        widget, label, initial, help_text, *args, **kwargs)