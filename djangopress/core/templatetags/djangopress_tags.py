from django.conf import settings

from django import template
register = template.Library()

def media_url():
    return settings.MEDIA_URL

register.simple_tag(media_url)
