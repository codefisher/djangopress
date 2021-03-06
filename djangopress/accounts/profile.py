
from djangopress.accounts.profiles import register, Profile, ProfileText
from djangopress.accounts.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from djangopress.accounts.forms import TimeZoneField
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __
from django.template.loader import render_to_string
from django.conf import settings
from PIL import Image
from django.core.files.images import get_image_dimensions

class ImageFileInput(forms.widgets.ClearableFileInput):
    template_with_initial = '%(initial)s %(clear_template)s %(input_text)s: %(input)s'
    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear)s %(clear_checkbox_label)s</label>'
    url_markup_template = '<img style="float:left; margin:0 1em;" alt="" src="{0}" />'

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
        widgets = {
                   'avatar': ImageFileInput(),
        }

    timezone = TimeZoneField(label=_("Time Zone"),
            help_text=__("For times to be displayed correctly you must select your locale timezone"))
    
    fieldsets = (
        ("Personality", ('homepage', 'avatar', 'signature')),
        ("Location", ('timezone', 'location')),
        ("Email", ('email_settings',)),
    )
    
    def clean_signature(self):
        signature = self.cleaned_data['signature']
        length = settings.ACCOUNTS_USER_LIMITS.get('signature', {}).get('length')
        if len(signature) > length:
            raise forms.ValidationError("Your signature can not be longer then %s characters." % length)
        num_lines = settings.ACCOUNTS_USER_LIMITS.get('signature', {}).get('lines')
        if num_lines and len(signature.splitlines()) > num_lines:
            raise forms.ValidationError("You can not have more then %s lines in your signature." % num_lines)
        return signature
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)
        size = settings.ACCOUNTS_USER_LIMITS.get('avatar', {}).get('size', 50)
        upload_size = settings.ACCOUNTS_USER_LIMITS.get('avatar', {}).get('max_upload_size', 200)
        file_size = settings.ACCOUNTS_USER_LIMITS.get('avatar', {}).get('file_size', 1024*100)
        if avatar:
            if avatar.size > file_size:
                raise forms.ValidationError("Image file too large")
            w, h = get_image_dimensions(avatar)
            if w > upload_size or h > upload_size:
                raise forms.ValidationError("Please user an image of size %s px by %s px" % (size, size))
        return avatar

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
                # needed for the image field, it needs a reload
                profile_form = UserProfileForm(instance=self._user.profile)
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