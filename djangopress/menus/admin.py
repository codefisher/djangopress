from django.contrib import admin
from djangopress.menus.models import Menu, MenuItem, StaticLink
from django import forms

class StaticLinkForm(forms.ModelForm):
    class Meta:
        model = StaticLink
        widgets = {
            'location': forms.TextInput()
        }

class StaticLinkAdmin(admin.ModelAdmin):
    form = StaticLinkForm

admin.site.register(StaticLink, StaticLinkAdmin)

class MenuAdmin(admin.ModelAdmin):
    pass
admin.site.register(Menu, MenuAdmin)

class MenuItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(MenuItem, MenuItemAdmin)