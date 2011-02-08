from django.conf.settings import MEDIA_URL

from django import template
register = template.Library()

def media_url():
    return MEDIA_URL

register.simple_tag(media_url)
