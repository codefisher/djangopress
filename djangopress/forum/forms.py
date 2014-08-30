from django import forms
from djangopress.forum.models import Thread, Post, Report


class ThreadForm(forms.ModelForm):
    class Meta(object):
        fields = ("subject",)
        model = Thread

class PostForm(forms.ModelForm):
    class Meta(object):
        fields = ("message","show_similies")
        model = Post
        
class PostAnonymousForm(forms.ModelForm):
    class Meta(object):
        fields = ("poster_name", "poster_email", "message","show_similies")
        model = Post
        
class PostEditForm(forms.ModelForm):
    class Meta(object):
        fields = ("message", "edit_reason", "show_similies")
        model = Post
        
class ReportForm(forms.ModelForm):
    class Meta(object):
        fields = ("message",)
        model = Report