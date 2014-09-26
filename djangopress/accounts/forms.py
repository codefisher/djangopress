import collections
import pytz
from django import forms
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __

"""
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
"""

zones = collections.defaultdict(list)
for zone in pytz.common_timezones:
    region, sep, city = zone.partition("/")
    zones[region].append((zone, zone.replace("_", " ").partition("/")[2].replace('/', ' ')))
long_zones = sorted([(region, list(sorted(items)))
                        for region, items in zones.items()
                    ])

class TimeZoneField(forms.ChoiceField):
    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text=None, *args, **kwargs):
        super(TimeZoneField, self).__init__(long_zones, required,
                        widget, label, initial, help_text, *args, **kwargs)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'email2',
                  'timezone', 'captcha')
    
    password1 = forms.CharField(label=__("Password"),
            widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=__("Confirm Password"),
            widget=forms.PasswordInput(render_value=False))

    email = forms.CharField(label=__("Email"))
    email2 = forms.CharField(label=__("Confirm Email"))

    timezone = TimeZoneField(label=_("Time Zone"),
            help_text=__("For times to be displayed correctly you must select your locale timezone"))

    #remember_between_visits = forms.BooleanField(initial=True)
    captcha = ReCaptchaField(label='')

    fieldsets = (
        ("User Name & Password", ('username', 'password1', 'password2')),
        ("Email", ('email', 'email2')),
        ("Location", ('timezone',)),
        ('Verification', ('captcha', ))
        #("Privacy", ('remember_between_visits',)),
    )

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data.get('username'))
            raise forms.ValidationError(_("User name already in use"))
        except User.DoesNotExist:
            pass
        return self.cleaned_data.get('username')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(u'This email address is already in use.')
        return email

    def clean_email2(self):
        if (self.cleaned_data.get('email') and self.cleaned_data.get('email2')
                and self.cleaned_data.get('email') != self.cleaned_data.get('email2')):
            raise forms.ValidationError(_("Emails must match"))
        return self.cleaned_data.get('email2')

    def clean_password2(self):
        if (self.cleaned_data.get('password1') and self.cleaned_data.get('password2')
                and self.cleaned_data.get('password1') != self.cleaned_data.get('password2')):
            raise forms.ValidationError(_("Passwords must match"))
        return self.cleaned_data.get('password2')