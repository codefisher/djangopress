from django import template
from django.core.urlresolvers import reverse
try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from djangopress.core.format.library import Library

register = template.Library()

def remove_netloc(url):
    parsed = urlparse(url)
    return urlunparse(('', '') + parsed[2:])

@register.simple_tag(takes_context=True)
def login_next(context, next_url):
    if not next_url or next_url == reverse('logout'):
        next_url = remove_netloc(context.get('request').META.get('HTTP_REFERER', ''))
        if next_url == reverse('logout'):
            next_url = "/"
    return next_url

@register.inclusion_tag('accounts/login_form.html', takes_context=True)
def login_form(context, next_url=None):
    return {
           "next": next_url if next_url else context['request'].path,
           "form":  AuthenticationForm(context['request']),
    }
    
@register.simple_tag(takes_context=True)
def show_signature(context, user):
    if not user.profile.signature:
        return ""
    try:
        use_images = settings.ACCOUNTS_USER_LIMITS.get('signature', {}).get('images', True)
        use_links = settings.ACCOUNTS_USER_LIMITS.get('signature', {}).get('links', True)
        bbcode = Library.get("bbcode").get("function")
        return bbcode(user.profile.signature, context=context, show_images=use_images, should_urlize=use_links, render_links=use_links)
    except:
        return ""