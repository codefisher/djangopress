from django import template
from django.core.urlresolvers import reverse
from urlparse import urlparse, urlunparse

register = template.Library()

def remove_netloc(url):
    parsed = urlparse(url)
    return urlunparse(('', '') + parsed[2:])

@register.simple_tag(takes_context=True)
def login_next(context, next_url):
    if not next_url or next_url == reverse('logout'):
        next_url = remove_netloc(context.get('request').META.get('HTTP_REFERER', ''))
    return next_url