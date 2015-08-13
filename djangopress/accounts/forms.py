import collections
import pytz
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __

if 'captcha' in settings.INSTALLED_APPS:
    from captcha.fields import ReCaptchaField
else:
    ReCaptchaField = None

zones = collections.defaultdict(list)
for zone in pytz.common_timezones:
    region, sep, city = zone.partition("/")
    zone_name = zone.replace("_", " ").partition("/")[2].replace('/', ' ')
    if not zone_name:
        zone_name = zone
    zones[region].append((zone, zone_name))
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
        if ReCaptchaField:
            fields = ('username', 'password1', 'password2', 'email', 'email2',
                  'timezone', 'captcha')
        else:
            fields = ('username', 'password1', 'password2', 'email', 'email2',
                  'timezone')
    
    password1 = forms.CharField(label=__("Password"),
            widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=__("Confirm Password"),
            widget=forms.PasswordInput(render_value=False))

    email = forms.CharField(label=__("Email"))
    email2 = forms.CharField(label=__("Confirm Email"))

    timezone = TimeZoneField(label=_("Time Zone"),
            help_text=__("For times to be displayed correctly you must select your locale timezone"))

    #remember_between_visits = forms.BooleanField(initial=True)
    if ReCaptchaField:
        captcha = ReCaptchaField(label='')

        fieldsets = (
            ("User Name & Password", ('username', 'password1', 'password2')),
            ("Email", ('email', 'email2')),
            ("Location", ('timezone',)),
            ('Verification', ('captcha', ))
            #("Privacy", ('remember_between_visits',)),
        )
    else:
        fieldsets = (
            ("User Name & Password", ('username', 'password1', 'password2')),
            ("Email", ('email', 'email2')),
            ("Location", ('timezone',)),
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