# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db import models
from djangopress.accounts.models import UserProfile
from djangopress.accounts.forms import TimeZoneField
from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.core.urlresolvers import reverse

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label=__("Password"),
            widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=__("Confirm Password"),
            widget=forms.PasswordInput(render_value=False))

    email = forms.CharField(label=__("Email"))
    email2 = forms.CharField(label=__("Confirm Email"))

    timezone = TimeZoneField(label=_("Time Zone"), initial="Etc/GMT-8",
            help_text=__("For times to be displayed correctly you must select your locale timezone"))

    remember_between_visits = forms.BooleanField(initial=True)

    fieldsets = (
        ("User Name & Password", ('username', 'password1', 'password2')),
        ("Email", ('email', 'email2')),
        ("Location", ('timezone',)),
        ("Privacy", ('remember_between_visits',)),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'email2',
                  'timezone', 'remember_between_visits')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_("User name already in use"))
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']

    def clean_email2(self):
        if (self.cleaned_data['email'] and self.cleaned_data['email2']
                and self.cleaned_data['email'] != self.cleaned_data['email2']):
            raise forms.ValidationError(_("Emails must match"))
        return self.cleaned_data['email2']

    def clean_password2(self):
        if (self.cleaned_data['password1'] and self.cleaned_data['password2']
                and self.cleaned_data['password1'] != self.cleaned_data['password2']):
            raise forms.ValidationError(_("Passwords must match"))
        return self.cleaned_data['password2']

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(True)
            user.is_active = False # set to true once they confirm email
            user.set_password(form.cleaned_data["password1"])
            user.save()
            profile = user.get_profile()
            profile.remember_between_visits = form.cleaned_data["remember_between_visits"]
            profile.timezone = form.cleaned_data["timezone"]
            client_address = request.META.get('HTTP_X_FORWARDED_FOR',
                    request.META.get("REMOTE_ADDR"))
            profile.registration_ip = client_address
            profile.last_ip_used = client_address
            profile.save()
            return HttpResponseRedirect(reverse('accounts-registered-message'))
    else:
        form = UserForm()
    data = {
        "form": form
    }
    return render_to_response("accounts/register.html" , data,
            context_instance=RequestContext(request))