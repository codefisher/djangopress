from django.contrib import admin
from djangopress.core.links.models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('label_text', 'location')

admin.site.register(Link, LinkAdmin)