
from djangopress.accounts.profiles import register, Profile, ProfileText
from djangopress.accounts.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from djangopress.accounts.forms import TimeZoneField
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.template.loader import render_to_string

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("first_name", "last_name")

    fieldsets = (
        ("Name", ('first_name', 'last_name')),
    )
    
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('homepage', 'avatar', 'signature', 'timezone', 'location', 'email_settings')

    timezone = TimeZoneField(label=_("Time Zone"),
            help_text=__("For times to be displayed correctly you must select your locale timezone"))
    
    fieldsets = (
        ("Personality", ('homepage', 'avatar', 'signature')),
        ("Location", ('timezone', 'location')),
        ("Email", ('email_settings',)),
    )

class UserProfile(Profile):
    label = "User Settings"
    
    def info(self):
        return {
                "position": -1,
                "template": "accounts/profile.html",
                "title": "Personal",
                "data": {
                       
                }
        }
        
    def edit(self, request):
        if request.method == 'POST':
            form = UserForm(request.POST, instance=self._user)
            if form.is_valid():
                form.save(True)
        else:
            form = UserForm(instance=self._user)
        if request.method == 'POST':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=self._user.profile)
            if profile_form.is_valid():
                profile_form.save(True)
        else:
            profile_form = UserProfileForm(instance=self._user.profile)
        change_password = render_to_string("accounts/profile_password.html", {"user": self._user})
        return {
                "position": -1,
                "forms": [form, ProfileText(change_password), profile_form],
        }
    
    def admin(self, request):
        pass
    
register('user', UserProfile, position=-1)