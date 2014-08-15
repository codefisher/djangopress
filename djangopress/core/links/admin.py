from django.contrib import admin
from djangopress.core.links.models import StaticLink
from django import forms

class StaticLinkForm(forms.ModelForm):
    class Meta:
        model = StaticLink
        widgets = {
            'location': forms.TextInput()
        }

class StaticLinkAdmin(admin.ModelAdmin):
    form = StaticLinkForm
    list_display = ('label_text', 'location')

admin.site.register(StaticLink, StaticLinkAdmin)