from django import template
from django.core.urlresolvers import reverse
from urlparse import urlparse, urlunparse
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()

def remove_netloc(url):
    parsed = urlparse(url)
    return urlunparse(('', '') + parsed[2:])

@register.simple_tag(takes_context=True)
def login_next(context, next_url):
    if not next_url or next_url == reverse('logout'):
        next_url = remove_netloc(context.get('request').META.get('HTTP_REFERER', ''))
    return next_url

@register.inclusion_tag('accounts/login_form.html', takes_context=True)
def login_form(context, next_url=None):
    return {
           "next": next_url if next_url else context['request'].path,
           "form":  AuthenticationForm(context['request']),
    }