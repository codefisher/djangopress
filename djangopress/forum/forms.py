from django import forms
from djangopress.forum.models import Thread, Post, Report
from django.conf import settings
from importlib import import_module

if hasattr(settings, 'CAPTCHA_APP') and settings.CAPTCHA_APP in settings.INSTALLED_APPS:
    fields = import_module("{}.fields".format(settings.CAPTCHA_APP))
    ReCaptchaField = fields.ReCaptchaField
else:
    ReCaptchaField = None

class ThreadForm(forms.ModelForm):
    class Meta(object):
        fields = ("subject",)
        model = Thread

class PostForm(forms.ModelForm):
    class Meta(object):
        fields = ("message","show_similies")
        model = Post
        
class QuickPostForm(PostForm):
    
    def __init__(self, *args, **kwargs):
        super(QuickPostForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget = forms.Textarea(attrs={'rows':4})
        self.fields['show_similies'].widget = forms.HiddenInput()
    
          
class PostAnonymousForm(forms.ModelForm):
    if ReCaptchaField:
        captcha = ReCaptchaField(label='')

    class Meta(object):
        if ReCaptchaField:
            fields = ("poster_name", "poster_email", "message", "show_similies", "captcha")
        else:
            fields = ("poster_name", "poster_email", "message", "show_similies")
        model = Post
        
    def __init__(self, *args, **kwargs):
        super(PostAnonymousForm, self).__init__(*args, **kwargs)
        self.fields['poster_name'].required = True
        self.fields['poster_email'].required = True
        
class PostEditForm(forms.ModelForm):
    class Meta(object):
        fields = ("message", "edit_reason", "show_similies")
        model = Post
        
class ReportForm(forms.ModelForm):
    class Meta(object):
        fields = ("message",)
        model = Report