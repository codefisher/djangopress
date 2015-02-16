from django.contrib import admin
from djangopress.theme.models import Theme

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'slug', 'active', 'name')
admin.site.register(Theme, ThemeAdmin)